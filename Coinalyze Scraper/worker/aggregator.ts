import { AggregatedTrade, AggregatorPayload, AggregatorSettings, Connection, Trade, Volumes } from '@/types/test'
import { exchanges, getExchangeById } from './exchanges'
import { parseMarket } from './helpers/utils'

const ctx: Worker = self as any

class Aggregator {
  settings: AggregatorSettings = {
    calculateSlippage: null,
    aggregationLength: null,
    preferQuoteCurrencySize: null,
    buckets: {}
  }
  connections: { [name: string]: Connection } = {}

  activeBuckets: string[] = []
  buckets: { [id: string]: Volumes } = {}
  connectionsCount = 0
  connectionChange: { [id: string]: number } = {}

  private onGoingAggregations: { [identifier: string]: AggregatedTrade } = {}
  private pendingTrades: Trade[] = []
  private marketsPrices: { [marketId: string]: number } = {}
  private _connectionChangeNoticeTimeout: number

  constructor() {
    console.info(`new worker instance`)

    this.bindExchanges()
    this.startPriceInterval()

    ctx.postMessage({
      op: 'hello'
    })
  }

  bindExchanges() {
    for (const exchange of exchanges) {
      exchange.on('subscribed', this.onSubscribed.bind(this, exchange.id))
      exchange.on('unsubscribed', this.onUnsubscribed.bind(this, exchange.id))
      exchange.on('error', this.onError.bind(this, exchange.id))
    }
  }

  bindTradesEvent() {
    for (const exchange of exchanges) {
      exchange.off('trades')

      if (this.settings.aggregationLength > 0) {
        exchange.on('trades', this.aggregateTrades.bind(this))
        exchange.on('liquidations', this.aggregateLiquidations.bind(this))
      } else {
        exchange.on('trades', this.emitTrades.bind(this))
        exchange.on('liquidations', this.emitLiquidations.bind(this))
      }
    }

    if (this.settings.aggregationLength > 0) {
      this.startAggrInterval()
      console.debug(`[worker] bind trades: aggregation`)
    } else {
      this.clearInterval('aggr')

      // clear pending aggregations
      this.timeoutExpiredAggregations()
      this.emitPendingTrades()

      console.debug(`[worker] bind trades: simple`)
    }
  }

  updateBuckets(bucketsDefinition: { [bucketId: string]: string[] }) {
    const activeBuckets = [] // array of buckets IDs
    const bucketEnabledMarkets = [] // array of markets IDs

    console.log('[worker] update buckets using :', bucketsDefinition)
    console.debug('[worker] previous buckets :', { ...this.buckets }, this.activeBuckets)

    for (const bucketId in bucketsDefinition) {
      if (activeBuckets.indexOf(bucketId) === -1) {
        activeBuckets.push(bucketId)
      }

      if (!this.buckets[bucketId]) {
        console.debug('[worker] create bucket', bucketId)
        this.buckets[bucketId] = this.createBucket()
      }

      for (const market of bucketsDefinition[bucketId]) {
        if (bucketEnabledMarkets.indexOf(market) === -1) {
          bucketEnabledMarkets.push(market)
        }

        if (!this.connections[market]) {
          // connection referenced in bucket doesn't exists
          console.warn('attempted to activate bucket on inexistant connection', market)
          continue
        }

        if (this.connections[market].bucket) {
          // bucket already running
          continue
        }

        // create empty bucket for this market
        console.debug('[worker] create market bucket', market)
        this.connections[market].bucket = this.createBucket()
      }
    }

    for (const market in this.connections) {
      if (this.connections[market].bucket && bucketEnabledMarkets.indexOf(market) === -1) {
        // destroy market's bucket (not referenced any buckets anymore)
        console.log('[worker] remove market bucket', market)
        this.connections[market].bucket = null
      }
    }

    for (const oldBucketId in this.buckets) {
      if (activeBuckets.indexOf(oldBucketId) === -1) {
        // destroy bucket (does not exists in settings or was modified by user)
        console.log('[worker] remove bucket', oldBucketId)
        delete this.buckets[oldBucketId]
      }
    }

    console.log('[worker] finished updating buckets (active buckets: ', activeBuckets, ')')

    if (activeBuckets.length && !this.activeBuckets.length) {
      this.startStatsInterval()
    } else if (this.activeBuckets.length && !activeBuckets.length && this['_statsInterval']) {
      this.clearInterval('stats')
      this['_statsInterval'] = null
      console.debug(`[worker] stopped statsInterval timer`)
    }

    this.activeBuckets = activeBuckets
    this.settings.buckets = bucketsDefinition
  }

  emitTrades(trades: Trade[]) {
    for (let i = 0; i < trades.length; i++) {
      const trade = trades[i]
      const marketKey = trade.exchange + trade.pair

      if (!this.connections[marketKey]) {
        continue
      }

      if (this.settings.calculateSlippage) {
        trade.originalPrice = this.marketsPrices[marketKey] || trade.price
      }

      trade.count = 1

      this.marketsPrices[marketKey] = trade.price

      this.processTrade(trade)
    }

    ctx.postMessage({
      op: 'trades',
      data: trades
    })
  }

  aggregateTrades(trades: Trade[]) {
    const now = Date.now()

    for (let i = 0; i < trades.length; i++) {
      const trade = (trades[i] as unknown) as AggregatedTrade
      const marketKey = trade.exchange + trade.pair

      if (!this.connections[marketKey]) {
        continue
      }

      if (this.onGoingAggregations[marketKey]) {
        const aggTrade = this.onGoingAggregations[marketKey]

        if (aggTrade.timestamp + this.settings.aggregationLength > trade.timestamp && aggTrade.side === trade.side) {
          aggTrade.size += trade.size
          aggTrade.prices += trade.price * trade.size
          aggTrade.price = trade.price
          aggTrade.count++
          continue
        } else {
          this.pendingTrades.push(this.processTrade(aggTrade))
        }
      }

      trade.originalPrice = this.marketsPrices[marketKey] || trade.price

      this.marketsPrices[marketKey] = trade.price

      trade.count = 1
      trade.prices = trade.price * trade.size
      trade.timeout = now + 50
      this.onGoingAggregations[marketKey] = trade
    }
  }

  emitLiquidations(trades: Trade[]) {
    for (let i = 0; i < trades.length; i++) {
      const trade = trades[i]
      const marketKey = trade.exchange + trade.pair

      if (!this.connections[marketKey]) {
        continue
      }

      this.processLiquidation(trade)
    }

    ctx.postMessage({
      op: 'trades',
      data: trades
    })
  }

  aggregateLiquidations(trades: Trade[]) {
    const now = Date.now()

    for (let i = 0; i < trades.length; i++) {
      const trade = (trades[i] as unknown) as AggregatedTrade
      const marketKey = trade.exchange + trade.pair
      const tradeKey = 'liq_' + marketKey

      if (!this.connections[marketKey]) {
        continue
      }

      if (this.onGoingAggregations[tradeKey]) {
        const aggTrade = this.onGoingAggregations[tradeKey]

        if (aggTrade.timestamp + this.settings.aggregationLength > trade.timestamp && aggTrade.side === trade.side) {
          aggTrade.size += trade.size
          aggTrade.count++
          continue
        } else {
          this.pendingTrades.push(this.processLiquidation(aggTrade))
        }
      }

      trade.count = 1
      trade.timeout = now + 50
      this.onGoingAggregations[tradeKey] = trade
    }
  }

  processTrade(trade: Trade): Trade {
    const marketKey = trade.exchange + trade.pair

    if (this.settings.calculateSlippage) {
      if (this.settings.calculateSlippage === 'price') {
        trade.slippage = Math.round((trade.price - trade.originalPrice + Number.EPSILON) * 10) / 10
        if (Math.abs(trade.slippage) / trade.price < 0.00025) {
          trade.slippage = null
        }
      } else if (this.settings.calculateSlippage === 'bps') {
        if (trade.side === 'buy') {
          trade.slippage = Math.floor(((trade.price - trade.originalPrice) / trade.originalPrice) * 10000)
        } else {
          trade.slippage = Math.floor(((trade.originalPrice - trade.price) / trade.price) * 10000)
        }
      }
    }

    if (this.settings.aggregationLength > 0) {
      trade.price = Math.max(trade.price, trade.originalPrice)
    }

    if (this.connections[marketKey].bucket) {
      const size = (this.settings.preferQuoteCurrencySize ? trade.price : 1) * trade.size

      this.connections[marketKey].bucket['c' + trade.side] += trade.count
      this.connections[marketKey].bucket['v' + trade.side] += size
    }

    return trade
  }

  processLiquidation(trade: Trade): Trade {
    const marketKey = trade.exchange + trade.pair

    if (this.connections[marketKey].bucket) {
      const size = (this.settings.preferQuoteCurrencySize ? trade.price : 1) * trade.size

      this.connections[marketKey].bucket['l' + trade.side] += size
    }

    return trade
  }

  timeoutExpiredAggregations() {
    const now = Date.now()

    const tradeKeys = Object.keys(this.onGoingAggregations)

    for (let i = 0; i < tradeKeys.length; i++) {
      const aggTrade = this.onGoingAggregations[tradeKeys[i]]

      if (now > aggTrade.timeout) {
        if (aggTrade.liquidation) {
          this.pendingTrades.push(this.processLiquidation(aggTrade))
        } else {
          this.pendingTrades.push(this.processTrade(aggTrade))
        }

        delete this.onGoingAggregations[tradeKeys[i]]
      }
    }
  }

  emitPendingTrades() {
    if (this.settings.aggregationLength > 0) {
      this.timeoutExpiredAggregations()
    }

    if (this.pendingTrades.length) {
      ctx.postMessage({ op: 'trades', data: this.pendingTrades })

      this.pendingTrades.splice(0, this.pendingTrades.length)
    }
  }

  emitStats() {
    const timestamp = Date.now()

    for (const bucketId in this.settings.buckets) {
      for (const market of this.settings.buckets[bucketId]) {
        if (!this.connections[market]) {
          continue
        }

        this.buckets[bucketId].vbuy += this.connections[market].bucket.vbuy
        this.buckets[bucketId].vsell += this.connections[market].bucket.vsell
        this.buckets[bucketId].cbuy += this.connections[market].bucket.cbuy
        this.buckets[bucketId].csell += this.connections[market].bucket.csell
        this.buckets[bucketId].lbuy += this.connections[market].bucket.lbuy
        this.buckets[bucketId].lsell += this.connections[market].bucket.lsell
      }

      this.buckets[bucketId].timestamp = timestamp

      ctx.postMessage({ op: 'bucket-' + bucketId, data: this.buckets[bucketId] })

      this.clearBucket(this.buckets[bucketId])
    }

    for (const market in this.connections) {
      if (!this.connections[market].bucket) {
        continue
      }

      this.clearBucket(this.connections[market].bucket)
    }
  }

  emitPrices() {
    if (!this.connectionsCount) {
      return
    }

    ctx.postMessage({ op: 'prices', data: this.marketsPrices })
  }

  onSubscribed(exchangeId, pair) {
    const market = exchangeId + pair

    if (this.connections[market]) {
      return
    }

    this.connections[market] = {
      exchange: exchangeId,
      pair: pair,
      hit: 0,
      timestamp: null
    }

    this.connectionsCount = Object.keys(this.connections).length

    for (const bucketId in this.settings.buckets) {
      if (this.settings.buckets[bucketId].indexOf(market) !== -1) {
        console.debug(`[worker] create bucket for new connection ${market}`)
        this.connections[market].bucket = this.createBucket()
        break
      }
    }

    ctx.postMessage({
      op: 'connection',
      data: {
        pair,
        exchangeId
      }
    })

    this.noticeConnectionChange(exchangeId, 1)
  }

  noticeConnectionChange(exchangeId, change) {
    if (!this.connectionChange[exchangeId]) {
      this.connectionChange[exchangeId] = 0
    }
    this.connectionChange[exchangeId] += change

    if (!this.connectionChange[exchangeId]) {
      delete this.connectionChange[exchangeId]
    }

    if (this._connectionChangeNoticeTimeout) {
      clearTimeout(this._connectionChangeNoticeTimeout)
    }

    if (!Object.keys(this.connectionChange).length) {
      return
    }

    let total = 0

    const connectionsByExchanges = Object.keys(this.connections).reduce((output, id) => {
      const exchange = this.connections[id].exchange
      if (typeof output[exchange] === 'undefined') {
        output[exchange] = 0
      }

      output[exchange]++

      total++

      return output
    }, {})

    this._connectionChangeNoticeTimeout = setTimeout(() => {
      this._connectionChangeNoticeTimeout = null
      const messages = []
      for (const id in this.connectionChange) {
        const change = this.connectionChange[id]
        messages.push(
          (!connectionsByExchanges[id] ? '<strike>' : '') +
            (id + ': ' + (change > 0 ? '+' : '') + change) +
            (!connectionsByExchanges[id] ? '</strike>' : '')
        )

        delete this.connectionChange[id]
      }

      ctx.postMessage({
        op: 'notice',
        data: {
          id: 'connections',
          type: 'success',
          title: total + ' connections<br>' + messages.join('<br>')
        }
      })
    }, 3000)
  }

  createBucket(): Volumes {
    return {
      timestamp: null,
      vbuy: 0,
      vsell: 0,
      cbuy: 0,
      csell: 0,
      lbuy: 0,
      lsell: 0
    }
  }

  clearBucket(bucket: Volumes) {
    bucket.cbuy = bucket.csell = bucket.vbuy = bucket.vsell = bucket.lbuy = bucket.lsell = 0
  }

  onUnsubscribed(exchangeId, pair) {
    const identifier = exchangeId + pair

    if (this.onGoingAggregations[identifier]) {
      delete this.onGoingAggregations[identifier]
    }

    if (this.connections[identifier]) {
      delete this.connections[identifier]

      this.connectionsCount = Object.keys(this.connections).length

      ctx.postMessage({
        op: 'disconnection',
        data: {
          pair,
          exchangeId
        }
      })

      this.noticeConnectionChange(exchangeId, -1)
    }
  }

  onError(exchangeId, reason) {
    let message: string

    if (typeof reason === 'string') {
      message = reason
    } else if (reason.message) {
      message = reason.message
    }

    if (message) {
      ctx.postMessage({
        op: 'notice',
        data: {
          id: exchangeId + '-error',
          type: 'error',
          title: `${exchangeId} disconnected unexpectedly (${message})`
        }
      })
    }
  }

  /**
   * Trigger subscribe to pairs (settings.pairs) on all enabled exchanges
   * @param {string[]} pairs eg ['BTCUSD', 'FTX:BTC-PERP']
   * @returns {Promise<any>} promises of connections
   * @memberof Server
   */
  async connect(markets: string[], trackingId?: string) {
    console.log(`[aggregator] connect`, markets)

    const marketsByExchange = markets.reduce((output, market) => {
      const [exchangeId, pair] = parseMarket(market)

      if (!exchangeId || !pair) {
        return {}
      }

      if (!output[exchangeId]) {
        output[exchangeId] = []
      }

      if (output[exchangeId].indexOf(market) === -1) {
        output[exchangeId].push(market)
      }

      return output
    }, {})

    const promises: Promise<any>[] = []

    for (const exchangeId in marketsByExchange) {
      const exchange = getExchangeById(exchangeId)

      if (exchange) {
        if (exchange.requireProducts) {
          await exchange.getProducts()
        }

        promises.push(
          (async () => {
            for (const market of marketsByExchange[exchangeId]) {
              await exchange.link(market)
            }
          })()
        )
      } else {
        console.error(`[worker.connect] unknown exchange ${exchangeId}`)
      }
    }

    await Promise.all(promises)

    if (trackingId) {
      ctx.postMessage({
        op: 'connect',
        trackingId
      })
    }
  }

  /**
   * Trigger unsubscribe to pairs on all activated exchanges
   * @param {string[]} pairs
   * @returns {Promise<void>} promises of disconnection
   * @memberof Server
   */
  async disconnect(markets: string[], trackingId?: string) {
    console.log(`[aggregator] disconnect`, markets)

    const marketsByExchange = markets.reduce((output, market) => {
      const [exchangeId, pair] = parseMarket(market)

      if (!exchangeId || !pair) {
        return {}
      }

      if (!output[exchangeId]) {
        output[exchangeId] = []
      }

      if (output[exchangeId].indexOf(market) === -1) {
        output[exchangeId].push(market)
      }

      return output
    }, {})

    const promises: Promise<void>[] = []

    for (const exchangeId in marketsByExchange) {
      const exchange = getExchangeById(exchangeId)

      if (exchange) {
        promises.push(
          (async () => {
            for (const market of marketsByExchange[exchangeId]) {
              await exchange.unlink(market)
            }
          })()
        )
      }
    }

    await Promise.all(promises)

    if (trackingId) {
      ctx.postMessage({
        op: 'connect',
        trackingId
      })
    }
  }

  startPriceInterval() {
    if (this['_priceInterval']) {
      return
    }
    this['_priceInterval'] = self.setInterval(this.emitPrices.bind(this), 1000)
  }

  startAggrInterval() {
    if (this['_aggrInterval']) {
      return
    }
    this['_aggrInterval'] = self.setInterval(this.emitPendingTrades.bind(this), 50)
  }

  startStatsInterval() {
    if (this['_statsInterval']) {
      return
    }
    this['_statsInterval'] = self.setInterval(this.emitStats.bind(this), 500)
  }

  clearInterval(name: string) {
    if (this['_' + name + 'Interval']) {
      clearInterval(this['_' + name + 'Interval'])
      this['_' + name + 'Interval'] = null
    }
  }

  async getExchangeProducts({ exchangeId, data }) {
    const exchange = getExchangeById(exchangeId)

    if (exchange.setProducts(data) === false) {
      await exchange.getProducts(true)
    }
  }

  async fetchExchangeProducts({ exchangeId, forceFetch }: { exchangeId: string; forceFetch?: boolean }, trackingId) {
    await getExchangeById(exchangeId).getProducts(forceFetch)

    ctx.postMessage({
      op: 'fetchExchangeProducts',
      trackingId: trackingId
    })
  }

  formatExchangeProducts({ exchangeId, response }, trackingId: string) {
    const productsData = getExchangeById(exchangeId).formatProducts(response)

    ctx.postMessage({
      op: 'formatExchangeProducts',
      data: productsData,
      trackingId: trackingId
    })
  }

  configureAggregator({ key, value }) {
    if (this.settings[key] === value) {
      return
    }

    this.settings[key] = value

    if (key === 'aggregationLength') {
      // update trades event handler (if 0 mean simple trade emit else group inc trades)
      this.bindTradesEvent()
    }
  }

  getHits(data, trackingId: string) {
    ctx.postMessage({
      op: 'getHits',
      trackingId: trackingId,
      data: exchanges.reduce((hits, exchanges) => hits + exchanges.count, 0)
    })
  }
}

const aggregator = new Aggregator()

self.addEventListener('message', (event: any) => {
  const payload = event.data as AggregatorPayload
  aggregator[payload.op](payload.data, payload.trackingId)
})

export default null
