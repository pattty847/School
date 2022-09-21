from json import load
import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg
from pycoingecko import CoinGeckoAPI
from pprint import pprint
import pandas as pd
from datetime import datetime


class Window():
    def __init__(self):
        self.WIDTH = 1600
        self.HEIGHT = 800

        self.title = 'TradeSuite'

        self.init_window()


    def init_window(self):
        with dpg.window(id='main', label='TradeSuite', width=self.WIDTH, height=self.HEIGHT):
            dpg.add_text('dsafasdfsadfasdfasd')

        dpg.set_primary_window('main', True)
        dpg.start_dearpygui()

























cg = CoinGeckoAPI()
btc = cg.get_coin_ohlc_by_id('bitcoin', vs_currency='usd', days=90)
df = pd.DataFrame(btc)
df.rename(columns={0: 'unix', 1: 'open', 2: 'high',
          3: 'low', 4: 'close'}, inplace=True)
df['date'] = pd.to_datetime(df['unix'], unit='ms')
coins = []
shares = []
test = {}
portfolio = pd.DataFrame(
    columns=['Coins', 'Shares', 'Purchase Price', 'Initial Investment', 'Value'])

# Main program viewport
vp = dpg.create_viewport(title='TradeSuite', width=1600, height=1200)
dpg.setup_dearpygui(viewport=vp)


def load_portfolio():
    pass


def create_index():
    pass


# TradeSuite homepage which is called after the __main__ python function runs
def start_viewport():
    # We create the Primary Window called 'candlestick-chart' which we can push information to later using parent
    with dpg.window(id="main-viewport", label="TradeSuite"):

        with dpg.menu_bar():

            with dpg.menu(label='View'):
                with dpg.menu(label='Crypto'):
                    dpg.add_menu_item(label='Portfolio',
                                      callback=load_portfolio)
                    dpg.add_menu_item(label='Create Index',
                                      callback=create_index)
                    dpg.add_menu_item(label='Ideas')
                    dpg.add_menu_item(label='Market')

                with dpg.menu(label='Stocks'):
                    dpg.add_menu_item(label='Portfolio')
                    dpg.add_menu_item(label='Charts')
                    dpg.add_menu_item(label='Ideas')
                    dpg.add_menu_item(label='Market')

            with dpg.menu(label='File'):
                dpg.add_menu_item(label='Item 1')
            with dpg.menu(label='File'):
                dpg.add_menu_item(label='Item 1')

        # input text box where we grab a cryptocurrency from the user
        dpg.add_input_text(id="input", label='Enter a Crypto')
        dpg.add_button(label="Search Coin Price")