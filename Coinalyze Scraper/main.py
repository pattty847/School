import ccxt
from pprint import pprint
import pandas as pd
from configparser import ConfigParser
import numpy as np
import matplotlib.pyplot as plt
import time

# from variable id
exchange_id = 'gateio'
exchange_class = getattr(ccxt, exchange_id)
gate_cred = ConfigParser()
gate_cred.read('C:\\Users\\pattt\\Desktop\\exchanges.config')
gate = exchange_class({
    'apiKey': gate_cred['GATEIO']['apiKey'],
    'secret': gate_cred['GATEIO']['secret'],
})

# gate_markets = gate.load_markets()
# print(gate.id, gate_markets)
        
# This function will calculate the WaveTrend and return them
def calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel, history):
    # Load the data from 'coin' by 'timeframe' (1000 lines 0-999)
    tfSrc = pd.DataFrame(gate.fetch_ohlcv(coin, timeframe))
    tfSrc.rename(columns= {
        0: 'Time', 
        1: 'Open',
        2: 'High',
        3: 'Low',
        4: 'Close',
        5: 'Volume'}, inplace=True, errors='raise')

    # Calculate the HLC (high low close) mean
    tfSrc['HLC3'] = (tfSrc['High'] + tfSrc['Low'] + tfSrc['Close']) / 3

    # ESA = Exponential Moving Average
    tfSrc['ESA'] = tfSrc.HLC3.ewm(span=chlen, adjust=False).mean()

    # de = ema(abs(tfsrc - esa), chlen)
    tfSrc['DE'] = abs(tfSrc.HLC3 - tfSrc.ESA).ewm(span=chlen, adjust=False).mean()

    # ci = (tfsrc - esa) / (0.015 * de)
    tfSrc['CI'] = (tfSrc.HLC3 - tfSrc.ESA) / (0.015 * tfSrc.DE)
    
    # wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
    tfSrc['wt1'] = tfSrc.CI.ewm(span=avg, adjust=False).mean()

    # wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
    tfSrc['wt2'] = tfSrc.wt1.rolling(malen).mean()

    tfSrc['wtVwap'] = tfSrc.wt1 - tfSrc.wt2
    
    tfSrc['wtOversold'] = tfSrc.wt2 <= oslevel
    tfSrc['wtOverbought'] = tfSrc.wt2 >= oblevel

    # see crossing(x, y) function
    tfSrc['wtCross'] = crossing(tfSrc['wt1'], tfSrc['wt2'])

    # determines if the cross above is bullish by being <= 0
    tfSrc['wtCrossUp'] = tfSrc['wt2'] - tfSrc['wt1'] <= 0

    # determines if the cross above is bearish by being <= 0
    tfSrc['wtCrossDown'] = tfSrc['wt2'] - tfSrc['wt1'] >= 0

    # see crossing(x, y) function (passing the series shifted to determine if the last row was a cross)
    tfSrc['wtCrosslast'] = crossing(tfSrc['wt1'].shift(-1), tfSrc['wt2'].shift(-1))

    tfSrc['wtCrossUplast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) <= 0
    tfSrc['wtCrossDownlast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) >= 0

    # Buy signal.
    tfSrc['Buy'] = tfSrc['wtCross'] & tfSrc['wtCrossUp'] & tfSrc['wtOversold']

    # Sell signal
    tfSrc['Sell'] = tfSrc['wtCross'] & tfSrc['wtCrossDown'] & tfSrc['wtOverbought']

    # return the waveTrend DataFrame or return the last minute
    return tfSrc if history else tfSrc[-1:]


def crossing(x, y):
    wtCross = []
    for i in range(len(x)):
        # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
        if(x.iloc[i] > y.iloc[i] and x.iloc[i-1] < y.iloc[i-1]) | (x.iloc[i] < y.iloc[i] and x.iloc[i-1] > y.iloc[i-1]):
            wtCross.append(True)
        else:
            wtCross.append(False)
    return wtCross


def checkForTrade(wt, coin, trade_ratio):
    # This will grab the orderbook for the coin
    orderbook = gate.fetch_order_book(coin)

    # this will grab the last close in the 
    last_close = wt.Close.iloc[-1]

    # trade size is the account balance * the trade ratio
    trade_size = gate.fetch_balance()[coin.split('/')[1]]['free'] * trade_ratio
    limit_order_placement = 0

    if(wt.Buy.any() == True):
        limit_order_placement =  gate.create_limit_buy_order(coin, (trade_size / last_close), last_close)
    elif(wt.Sell.any() == True):
        limit_order_placement =  gate.create_limit_sell_order(coin, (trade_size / last_close), last_close)
    return limit_order_placement


if __name__ == "__main__":
    # calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel)

    coin = 'BTC'
    currency = 'USDT'
    pair = coin + '/' + currency
    timeframe = '1m'
    trade_ratio_to_balance = .3 # 30% of account balance to be used / trade

    # waveTrend = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, True)
    lastMinuteWT = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, False)

    while(True):
        order = checkForTrade(lastMinuteWT, pair, trade_ratio_to_balance)

        #waveTrend.to_csv('wavetrend.csv')
        pprint(lastMinuteWT)
        print(order)

        time.sleep(4)