import Exchange from '../exchange'

export default class extends Exchange {
  id = 'BITFINEX'
  private lastSubscriptionId = 0
  private channels = {}
  private prices = {}
  protected endpoints = { PRODUCTS: 'https://api.bitfinex.com/v1/symbols' }

  getUrl() {
    return 'wss://api-pub.bitfinex.com/ws/2/'
  }

  formatProducts(pairs) {
    return pairs.map(product => product.toUpperCase())
  }

  /**
   * Sub
   * @param {WebSocket} api
   * @param {string} pair
   */
  async subscribe(api, pair) {
    if (!(await super.subscribe(api, pair))) {
      return
    }

    api.send(
      JSON.stringify({
        event: 'subscribe',
        channel: 'trades',
        symbol: 't' + pair
      })
    )

    if (api._connected.length === 1) {
      api.send(
        JSON.stringify({
          event: 'subscribe',
          channel: 'status',
          key: 'liq:global'
        })
      )
    }

    return true
  }

  /**
   * Unsub
   * @param {WebSocket} api
   * @param {string} pair
   */
  async unsubscribe(api, pair) {
    if (!(await super.unsubscribe(api, pair))) {
      return
    }

    if (api._connected.length === 0) {
      const chanId = Object.keys(this.channels).find(id => this.channels[id].name === 'status')

      if (chanId) {
        api.send(
          JSON.stringify({
            event: 'unsubscribe',
            chanId: chanId
          })
        )

        delete this.channels[chanId]
      }

      return true
    }

    const channelsToUnsubscribe = Object.keys(this.channels).filter(id => this.channels[id].pair === pair)

    if (!channelsToUnsubscribe.length) {
      console.log(
        `[${this}.id}/unsubscribe] no channel to unsubscribe to, but server called unsubscibr(${pair}). Here is the active channels on bitfinex exchange :`,
        this.channels
      )
      return
    }

    for (const id of channelsToUnsubscribe) {
      api.send(
        JSON.stringify({
          event: 'unsubscribe',
          chanId: id
        })
      )

      delete this.channels[id]
    }
  }

  onMessage(event, api) {
    const json = JSON.parse(event.data)

    if (json.event === 'subscribed' && json.chanId) {
      console.debug(`[${this.id}] register channel ${json.chanId} (${json.channel}:${json.pair})`)
      this.channels[json.chanId] = {
        name: json.channel,
        pair: json.pair
      }
      return
    }

    if (!this.channels[json[0]] || json[1] === 'hb') {
      if (json[1] !== 'hb' && json.event !== 'info') {
        console.warn(`[${this.id}] received unknown event ${event.data}`)
      }
      return
    }

    const channel = this.channels[json[0]]

    if (!channel.hasSentInitialMessage) {
      console.debug(`[${this.id}] skip first payload ${channel.name}:${channel.pair}`)
      channel.hasSentInitialMessage = true
      return
    }

    if (channel.name === 'trades' && json[1] === 'te') {
      this.prices[api.id + channel.pair] = +json[2][3]

      return this.emitTrades(api.id, [
        {
          exchange: this.id,
          pair: channel.pair,
          timestamp: +new Date(json[2][1]),
          price: +json[2][3],
          size: Math.abs(json[2][2]),
          side: json[2][2] < 0 ? 'sell' : 'buy'
        }
      ])
    } else if (channel.name === 'status' && json[1]) {
      return this.emitLiquidations(
        api.id,
        json[1]
          .filter(a => api._connected.indexOf(a[4].substring(1)) !== -1)
          .map(a => {
            const pair = a[4].substring(1)

            return {
              exchange: this.id,
              pair: a[4].substring(1),
              timestamp: parseInt(a[2]),
              price: this.prices[api.id + pair],
              size: Math.abs(a[5]),
              side: a[5] > 1 ? 'sell' : 'buy',
              liquidation: true
            }
          })
      )
    }
  }
}
