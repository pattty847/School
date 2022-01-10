import ccxt
import time
from pprint import pprint
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import math
from configparser import ConfigParser


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


"""
// WaveTrend
    wtShow = input(true, title = 'Show WaveTrend', type = input.bool)
    wtBuyShow = input(true, title = 'Show Buy dots', type = input.bool)
    wtGoldShow = input(true, title = 'Show Gold dots', type = input.bool)
    wtSellShow = input(true, title = 'Show Sell dots', type = input.bool)
    wtDivShow = input(true, title = 'Show Div. dots', type = input.bool)
    vwapShow = input(true, title = 'Show Fast WT', type = input.bool)
    wtChannelLen = input(9, title = 'WT Channel Length', type = input.integer)
    wtAverageLen = input(12, title = 'WT Average Length', type = input.integer)
    wtMASource = input(hlc3, title = 'WT MA Source', type = input.source)
    wtMALen = input(3, title = 'WT MA Length', type = input.integer)
    [wt1, wt2, wtOversold, wtOverbought, wtCross, wtCrossUp, wtCrossDown, wtCrosslast, wtCrossUplast, wtCrossDownlast, wtVwap]
"""

# This function will calculate the WaveTrend and return them
""" Wave Trend:
    tfsrc = security(syminfo.tickerid, tf, src)
    esa = ema(tfsrc, chlen)
    de = ema(abs(tfsrc - esa), chlen)
    ci = (tfsrc - esa) / (0.015 * de)
    wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
    wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
    wtVwap = wt1 - wt2
    wtOversold = wt2 <= osLevel
    wtOverbought = wt2 >= obLevel
    wtCross = cross(wt1, wt2)
    wtCrossUp = wt2 - wt1 <= 0
    wtCrossDown = wt2 - wt1 >= 0
    wtCrosslast = cross(wt1[2], wt2[2])
    wtCrossUplast = wt2[2] - wt1[2] <= 0
    wtCrossDownlast = wt2[2] - wt1[2] >= 0
"""
def calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel):
    # Load the data from 'coin' by 'timeframe' (1000 lines 0-999)
    tfSrc = pd.DataFrame(gate.fetch_ohlcv(coin, timeframe))
    # this will check to see if the exchange sent the last minute. Sometimes the tfSrc DataFrame will only give 999/1000 rows
    # we need to check the last index to make sure it's 999.
    while(tfSrc.index[-1] != 999):
        tfSrc = pd.DataFrame(gate.fetch_ohlcv(coin, timeframe))
    tfSrc = dropna(tfSrc)
    tfSrc.rename(columns= {
        0: 'Time', 
        1: 'Open',
        2: 'High',
        3: 'Low',
        4: 'Close',
        5: 'Volume'}, inplace=True, errors='raise')

    tfSrc['HLC3'] = (tfSrc['High'] + tfSrc['Low'] + tfSrc['Close']) / 3

    # EMA = ( 2/n + 1 ) * (Close-Previous_EMA) + Previous_EMA
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
    
    # return the last minute
    return tfSrc[-1:]

def checkForTrade(wt):
    # Buy signal.
    buySignal = wt['wtCross'] and wt['wtCrossUp'] and wt['wtOversold']

    # buySignalDiv = (wtwtShowDiv and wtBullDiv) or 
    #            (wtShowDiv and wtBullDiv_add) or 
    #            (stochShowDiv and stochBullDiv) or 
    #            (rsiShowDiv and rsiBullDiv)
        
    # buySignalDiv_color = wtBullDiv ? colorGreen : 
    #                    wtBullDiv_add ? color.new(colorGreen, 60) : 
    #                    rsiShowDiv ? colorGreen : na

    # Sell signal
    sellSignal = wt['wtCross'] and wt['wtCrossDown'] and wt['wtOverbought']
                
    # sellSignalDiv = (wtShowDiv and wtBearDiv) or 
    #            (wtShowDiv and wtBearDiv_add) or
    #            (stochShowDiv and stochBearDiv) or
    #            (rsiShowDiv and rsiBearDiv)
                        
    # sellSignalDiv_color = wtBearDiv ? colorRed : 
    #                    wtBearDiv_add ? color.new(colorRed, 60) : 
    #                    rsiBearDiv ? colorRed : na

    # Gold Buy 
    # lastRsi = valuewhen(wtFractalBot, rsi[2], 0)[2]
    # wtGoldBuy = ((wtShowDiv and wtBullDiv) or (rsiShowDiv and rsiBullDiv)) and
    #        wtLow_prev <= osLevel3 and
    #        wt2 > osLevel3 and
    #        wtLow_prev - wt2 <= -5 and
    #        lastRsi < 30
    if(buySignal):
        pass


if __name__ == "__main__":
    # calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel)
    print(calculateWaveTrend("BTC/USDT", '1m',  9, 12, 3, -53, 53))