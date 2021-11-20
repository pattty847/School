import json
from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.graph_objects as go



cg = CoinGeckoAPI()

allCoinsAllMarkets = []
trendingCoinList = cg.get_search_trending()


with open('allCoins.json', 'r') as f:
    allCoinsAllMarkets = json.load(f)


def coinLookup(coin):
    return cg.get_coin_by_id(coin)

def coinHistory(coin, days):
    return cg.get_coin_ohlc_by_id(id=coin, vs_currency='usd', days=days)

harmonyOHLC = pd.DataFrame(coinHistory('harmony', '30'))
harmonyOHLC.rename(columns={0:'DATE', 1:'OPEN', 2:'HIGH', 3:'LOW', 4:'CLOSE'}, inplace=True, errors='raise')

OHLCChart = go.Figure(data=go.Ohlc(x=harmonyOHLC['DATE'],
                    open=harmonyOHLC['OPEN'],
                    high=harmonyOHLC['HIGH'],
                    low=harmonyOHLC['LOW'],
                    close=harmonyOHLC['CLOSE']))

OHLCChart.show()
print(harmonyOHLC.head())