import dearpygui.dearpygui as dpg
import pandas as pd
from pycoingecko import CoinGeckoAPI
import pprint

cg = CoinGeckoAPI()


coins = ["bitcoin", "ethereum", "solana", "avalance"]


trending_data = cg.get_search_trending()
trending_coins = []
coins_prices = []
for coins in trending_data["coins"]:
    price = cg.get_price(ids=coins["item"]["id"], vs_currencies='usd')
    trending_coins.append(coins["item"]["id"] + ":"+price)
    


with dpg.window(label="Trending Coins", id="terminal"):
    for each in trending_coins:
        dpg.add_text(each)


dpg.start_dearpygui()