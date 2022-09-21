import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import backtest


class WaveTrendStrategy(backtest):

    """Derives from Strategy to produce a set of signals that
    are randomly generated long/shorts. Clearly a nonsensical
    strategy, but perfectly acceptable for demonstrating the
    backtesting infrastructure!"""    
    
    def __init__(self, symbol, bars):
        """Requires the symbol ticker and the pandas DataFrame of bars"""
        self.symbol = symbol
        self.bars = bars


    # This function will calculate the WaveTrend and return them
    def calculateWaveTrend(coin, timeframe, chlen, avg, malen, oslevel, oblevel, history, exchange):
        # Load the data from 'coin' by 'timeframe' (1000 lines 0-999)
        # limit will show x bars of history
        tfSrc = pd.DataFrame(exchange.fetch_ohlcv(coin, timeframe, limit=30))
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



def crossing(x, y):
    wtCross = []
    for i in range(len(x)):
        # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
        if(x.iloc[i] > y.iloc[i] and x.iloc[i-1] < y.iloc[i-1]) | (x.iloc[i] < y.iloc[i] and x.iloc[i-1] > y.iloc[i-1]):
            wtCross.append(True)
        else:
            wtCross.append(False)
    return wtCross


"""
    def generate_signals(self):
        # Creates a pandas DataFrame of random signals.
        signals = pd.DataFrame(index=self.bars.index)
        signals['signal'] = np.sign(np.random.randn(len(signals)))

        # The first five elements are set to zero in order to minimise
        # upstream NaN errors in the forecaster.
        signals['signal'][0:5] = 0.0
        return signals
"""