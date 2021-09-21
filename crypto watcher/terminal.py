import dearpygui.dearpygui as dpg
import pandas as pd
from pycoingecko import CoinGeckoAPI
import pprint

cg = CoinGeckoAPI()


coins = ["bitcoin", "ethereum", "solana", "avalance"]


data = cg.get_search_trending()

