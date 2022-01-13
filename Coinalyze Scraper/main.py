import ccxt
import time
from pprint import pprint
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import math
from configparser import ConfigParser
import numpy as np
import matplotlib.pyplot as plt
import json

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

    # this will check to see if the exchange sent the last minute. Sometimes the tfSrc DataFrame will only give 999/1000 rows
    # we need to check the last index to make sure it's 999.
    # while(tfSrc.index[-1] != 999):
    #    tfSrc = pd.DataFrame(gate.fetch_ohlcv(coin, timeframe))

    tfSrc = dropna(tfSrc)
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
    tfSrc['ESA'] = tfSrc['HLC3'].ewm(span=chlen, adjust=False).mean()

    # de = ema(abs(tfsrc - esa), chlen)
    tfSrc['DE'] = abs(tfSrc.HLC3 - tfSrc['ESA']).ewm(span=chlen, adjust=False).mean()

    # ci = (tfsrc - esa) / (0.015 * de)
    tfSrc['CI'] = (tfSrc.HLC3 - tfSrc['ESA']) / (0.015 * tfSrc['DE'])
    
    # wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
    tfSrc['wt1'] = tfSrc['CI'].ewm(span=avg, adjust=False).mean()

    # wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
    tfSrc['wt2'] = tfSrc['wt1'].rolling(malen).mean()

    tfSrc['wtVwap'] = tfSrc['wt1'] - tfSrc['wt2']
    tfSrc['wtOversold'] = tfSrc['wt2'] <= oslevel
    tfSrc['wtOverbought'] = tfSrc['wt2'] >= oblevel
    tfSrc['wtCross'] = tfSrc['wt1'] >= tfSrc['wt2']
    tfSrc['wtCrossUp'] = tfSrc['wt2'] - tfSrc['wt1'] <= 0
    tfSrc['wtCrossDown'] = tfSrc['wt2'] - tfSrc['wt1'] >= 0
    tfSrc['wtCrosslast'] = tfSrc['wt1'][2] >= tfSrc['wt2'][2]
    tfSrc['wtCrossUplast'] = tfSrc['wt2'][2] - tfSrc['wt1'][2] <= 0
    tfSrc['wtCrossDownlast'] = tfSrc['wt2'][2] - tfSrc['wt1'][2] >= 0

    # Buy signal.
    # tfSrc['Buy'] = tfSrc['wtCross'] & tfSrc['wtCrossUp'] & tfSrc['wtOversold']

    # Sell signal
    # tfSrc['Sell'] = tfSrc['wtCross'] & tfSrc['wtCrossDown'] & tfSrc['wtOverbought']

    # return the last minute
    return tfSrc if history else tfSrc[-1:]

def crossing(x, y):
    if(x > y) and (x[1] < y[1]):
        return True
    else:
        return False


def checkForTrade(wt, coin, trade_ratio):
    # This will grab the orderbook for the coin
    orderbook = gate.fetch_order_book(coin)
    last_close = wt.Close.iloc[-1]

    # trade size is the account balance * the trade ratio
    trade_size = gate.fetch_balance()[coin.split('/')[1]]['free'] * trade_ratio

    pprint(trade_size / last_close)
    if(wt.Buy.any() == True):
        pass
        # limit_order_placement =  gate.create_limit_buy_order(coin, trade_size / last_close, '0.013')

    #return limit_order_placement


def plotLastData(df):
    df.plot(kind='line', x=df.Time, y=df.Close)
    plt.show()


if __name__ == "__main__":
    # calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel)

    coin = 'XPR'
    currency = 'USDT'
    pair = coin+'/'+currency
    timeframe = '5m'
    trade_ratio_to_balance = .3 # 10% of account balance to be used / trade

    waveTrend = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, True)
    lastMinuteWT = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, False)
    # plotLastData(waveTrend)
    # checkForTrade(waveTrend, pair, trade_ratio_to_balance)

    waveTrend.to_csv('wavetrend.csv')