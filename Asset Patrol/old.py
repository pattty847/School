from json import load
import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg
from pycoingecko import CoinGeckoAPI
from pprint import pprint
import pandas as pd
from datetime import datetime


cg = CoinGeckoAPI()
btc = cg.get_coin_ohlc_by_id('bitcoin', vs_currency='usd', days=90)
df = pd.DataFrame(btc)
df.rename(columns={0: 'unix', 1: 'open', 2: 'high', 3: 'low', 4: 'close'}, inplace=True)  
df['date'] = pd.to_datetime(df['unix'], unit='ms')
coins = []
shares = []
test = {}
portfolio = pd.DataFrame(columns=['Coins', 'Shares', 'Purchase Price', 'Initial Investment', 'Value'])

# Main program viewport
vp = dpg.create_viewport(title='TradeSuite', width=1600, height=1200)
dpg.setup_dearpygui(viewport=vp)


def getOHLC(sender, app_data, user_data):
    search_value = dpg.get_value('input')
    if(search_value == ""): return ""
    
    btc_OHLC = cg.get_coin_ohlc_by_id(search_value, vs_currency='usd', days=90)
    btc_df = pd.DataFrame(btc_OHLC)
    btc_df.rename(columns={0: 'volume', 1: 'open', 2: 'high', 3: 'low', 4: 'close'}, inplace=True)  
    with dpg.table(header_row=True, parent='candlestick-chart'):

            # use add_table_column to add columns to the table,
            # table columns use child slot 0
            dpg.add_table_column(label="Volume")
            dpg.add_table_column(label="Open")
            dpg.add_table_column(label="High")
            dpg.add_table_column(label="Low")
            dpg.add_table_column(label="Close")
            for i in range(0, btc_df.shape[0]):
                for j in range(0, btc_df.shape[1]):
                    dpg.add_text(btc_df.iloc[i, j])

                    # call if not last cell
                    if not (i == btc_df.shape[0] and j == btc_df.shape[1]):
                        dpg.add_table_next_column()


            # dpg.add_candle_series(dates=list(btc_df.index), opens=btc_df['open'], highs=btc_df['high'], lows=['low'], closes=['close'])


def draw_candleplot():
    for each in df['date']:
        print(each)

    dates = df['date'].to_numpy()
    highs = df['high'].to_numpy()
    lows = df['low'].to_numpy()
    opens = df['open'].to_numpy()
    closes = df['close'].to_numpy()
    min_dates = min(dates)
    max_dates = max(dates)
    max_highs = max(highs)
    min_lows = min(lows)
    # We create the Primary Window called 'candlestick-chart' which we can push information to later using parent
    with dpg.window(id = "candlestick-chart", label="TradeSuite"):

        # input text box where we grab a cryptocurrency from the user
        dpg.add_input_text(id="input", label='Enter a Crypto')
        dpg.add_button(label="Search Coin Price", callback=getOHLC)

        with dpg.plot(label='plot'):
            dpg.add_plot_legend()

            with dpg.add_plot_axis(dpg.mvXAxis, label="Dates", time=True):
                dpg.set_axis_limits(dpg.last_item(), float(min_dates), float(max_dates))

            with dpg.add_plot_axis(dpg.mvYAxis, label="Prices"):
                dpg.set_axis_limits(dpg.last_item(), float(min_lows), float(max_highs))

            dpg.add_candle_series(dates=dates, opens=opens, highs=highs, lows=lows, closes=closes, label="Candlesticks", parent="plot")


def load_portfolio():
    with dpg.window(id = 'portfolio', label='Portfolio', width=800, height=800, no_resize=True):
        # create plot
        with dpg.plot(label="Line Series", height=400, width=400):

            # optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", id="y_axis")

            dpg.add_pie_series(x=10.0, y=40.0, radius=50.0, values=['itemdsas', 'dsfasd', 'sfsadfa'], labels=['fdsa', 'sdfas', 'fdsafs'], parent=dpg.last_item())

# Callback/Window - This window will allow users to build a portfolio index that averages the total price of all coins * shares: coins * shares / coins.length
def create_index():

    with dpg.window(id='create-index', label='Create Index', width=800, height=800, no_resize=True):
        # input text box where we grab a cryptocurrency from the user
        dpg.add_input_text(id="crypto-index", label='Enter a Crypto', width=100)
        dpg.add_input_text(id="crypto-shares", label='# of Shares', width=100)
        dpg.add_same_line()
        dpg.add_button(label="Add Coin", callback=add_coin)
        dpg.add_same_line()
        dpg.add_button(label="Done", callback=create_portfolio)
        dpg.add_text(id='crypto-index-results-field')


# Callback/Function - this adds the list of coins to portfolio DataFrame after the user is done entering them
def create_portfolio():

    portfolio['Coins'] = coins
    portfolio['Shares'] = shares


    with dpg.window(id='loaded-portfolio', label='Portfolio Name', width=800, height=800, no_resize=True):

        with dpg.table(header_row=True, parent='candlestick-chart'):

            # use add_table_column to add columns to the table,
            # table columns use child slot 0
            for column in portfolio.columns:
                dpg.add_table_column(label = column)

            for i in range(0, portfolio.shape[0]):
                for j in range(0, portfolio.shape[1]):
                    dpg.add_text(portfolio.iloc[i, j])

                    # call if not last cell
                    if not (i == portfolio.shape[0] and j == portfolio.shape[1]):
                        dpg.add_table_next_column()


# Callback/Function - checks if the text area is blank or if the coin cannot be found, then adds it to the 'coins' list
def add_coin():

    if(dpg.get_value('crypto-index') == "" or dpg.get_value('crypto-shares') == "" or cg.get_price(dpg.get_value('crypto-index'), vs_currencies='usd') == {}): return print("Error finding coin.")
    shares_value = dpg.get_value("crypto-shares")
    try:
        int(shares_value)
    except ValueError as e:
        print(e + "Use a # for 'shares'")

    price = cg.get_price(dpg.get_value('crypto-index'), vs_currencies='usd')
    test[dpg.get_value('crypto-index')] = shares
    test["value"] = price[dpg.get_value('crypto-index')]['usd'] * shares
    print(test)

    dpg.set_value('crypto-index-results-field', dpg.get_value('crypto-index'))
    coins.append(dpg.get_value('crypto-index'))
    shares.append(shares_value)
    


# TradeSuite homepage which is called after the __main__ python function runs
def start_viewport():
    # We create the Primary Window called 'candlestick-chart' which we can push information to later using parent
    with dpg.window(id = "main-viewport", label="TradeSuite"):

        with dpg.menu_bar():
            
            with dpg.menu(label='View'):
                with dpg.menu(label='Crypto'):
                    dpg.add_menu_item(label='Portfolio', callback=load_portfolio)
                    dpg.add_menu_item(label='Create Index', callback=create_index)
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
        dpg.add_button(label="Search Coin Price", callback=getOHLC)


