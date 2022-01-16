from logging import exception
import time
from tkinter.tix import Tree
import ccxt
from pprint import pprint
import pandas as pd
from configparser import ConfigParser
import numpy as np
import matplotlib.pyplot as plt


# from variable id
#exchange_id = 'gateio'
#exchange_class = getattr(ccxt, exchange_id)
configFile = ConfigParser()
configFile.read('C:\\Users\\pattt\\Desktop\\exchanges.config')
#gate = exchange_class({
#    'apiKey': configFile['GATEIO']['apiKey'],
#    'secret': configFile['GATEIO']['secret'],
#})

def connectExchanges(exchange_list):
    results = {}
    xchange_class = []
    for i in exchange_list:
        exchange_class = getattr(ccxt, i)
        if(i.upper() in configFile):
            exchange = exchange_class({
                'apiKey': configFile[i.upper()]['apiKey'],
                'secret': configFile[i.upper()]['secret'],
            })
            print(type(exchange))
            xchange_class.append(exchange)
        else:
            xchange_class.append(exchange_class)

    for key, value in zip(exchange_list, xchange_class):
        results[key] = value

    return results


# gate_markets = gate.load_markets()
# print(gate.id, gate_markets)
        
# This function will calculate the WaveTrend and return them
def calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel, history, exchange):
    # Load the data from 'coin' by 'timeframe' (1000 lines 0-999)
    tfSrc = pd.DataFrame(exchange.fetch_ohlcv(coin, timeframe))
    tfSrc.rename(columns= {
        0: 'Time', 
        1: 'Open',
        2: 'High',
        3: 'Low',
        4: 'Close',
        5: 'Volume'}, inplace=True, errors='raise')
    tfSrc.dropna()

    tfSrc['Time'] = pd.to_datetime(tfSrc['Time'], unit='ms')

    # Calculate the HLC (high low close) mean
    tfSrc['HLC3'] = (tfSrc['High'] + tfSrc['Low'] + tfSrc['Close']) / 3

    # ESA = Exponential Moving Average
    tfSrc['ESA'] = tfSrc['HLC3'].ewm(span=chlen, adjust=False).mean()

    # de = ema(abs(tfsrc - esa), chlen)
    tfSrc['DE'] = abs(tfSrc['HLC3'] - tfSrc['ESA']).ewm(span=chlen, adjust=False).mean()

    # ci = (tfsrc - esa) / (0.015 * de)
    tfSrc['CI'] = (tfSrc['HLC3'] - tfSrc['ESA']) / (0.015 * tfSrc['DE'])
    
    # wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
    tfSrc['wt1'] = tfSrc['CI'].ewm(span=avg, adjust=False).mean()

    # wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
    tfSrc['wt2'] = tfSrc['wt1'].rolling(malen).mean()

    tfSrc['wtVwap'] = tfSrc['wt1'] - tfSrc['wt2']
    
    tfSrc['wtOversold'] = tfSrc['wt2'] <= oslevel
    tfSrc['wtOverbought'] = tfSrc['wt2'] >= oblevel

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


def topFractal(src):
    return src.shift(-4) < src.shift(-2) and src.shift(-3) < src.shift(-2) and src.shift(-2) > src.shift(-1) and src.shift(-2) > src

def botFractal(src):
    return src.shift(-4) > src.shift(-2) and src.shift(-3) > src.shift(-2) and src.shift(-2) < src.shift(-1) and src.shift(-2) < src



def crossing(x, y):
    wtCross = []
    for i in range(len(x)):
        # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
        if(x.iloc[i] >= y.iloc[i] and x.iloc[i-1] <= y.iloc[i-1]) | (x.iloc[i] <= y.iloc[i] and x.iloc[i-1] >= y.iloc[i-1]):
            wtCross.append(True)
        else:
            wtCross.append(False)
    return wtCross


def checkForTrade(wt, coin, trade_ratio, exchange):
    # This will grab the orderbook for the coin
    orderbook = exchange.fetch_order_book(coin)

    # this will grab the last close in the 
    last_close = wt.Close.iloc[-1]

    # trade size is the account balance * the trade ratio
    trade_size = exchange.fetch_balance()[coin.split('/')[1]]['free'] * trade_ratio
    limit_order_placement = "Not in trade"

    if(wt.Buy.any() == True):
        limit_order_placement =  exchange.create_limit_buy_order(coin, (trade_size / last_close), last_close + 10)
    elif(wt.Sell.any() == True):
        limit_order_placement =  exchange.create_limit_sell_order(coin, (trade_size / last_close), last_close - 10)
    return limit_order_placement


if __name__ == "__main__":
    # calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel)
    exchange_list = ['binance', 'gateio']
    exchange = connectExchanges(exchange_list)
    coin = 'BTC'
    currency = 'USDT'
    pair = coin + '/' + currency
    timeframe = '5m'
    trade_ratio_to_balance = .3 # 30% of account balance to be used / trade

    # waveTrend = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, True)
    # waveTrend.to_csv('wavetrend.csv')

    # pprint(exchange['binance'].fetch_tickers(['BTC/USDT']))

    while(True):
        try:
            lastMinuteWT = calculateWaveTrend(pair, timeframe,  9, 12, 3, -53, 53, False, exchange=exchange['gateio'])
            order = checkForTrade(lastMinuteWT, pair, trade_ratio_to_balance, exchange=exchange['gateio'])

            #waveTrend.to_csv('wavetrend.csv')
            pprint(lastMinuteWT)
            print(order)

            time.sleep(5)
        except ccxt.NetworkError as e:
            print(e)
        except ccxt.ExchangeError as e:
            print(e)
        except Exception as e:
            print(e)
