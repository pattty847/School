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


# Main program viewport
vp = dpg.create_viewport(title='TradeSuite', width=1600, height=1200)
dpg.setup_dearpygui(viewport=vp)


def getOHLC(sender, app_data, user_data):
    search_value = dpg.get_value('input')
    if(search_value != ""):
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

# TradeSuite homepage which is called after the __main__ python function runs
def start_viewport():
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





if(__name__ == "__main__"):
    start_viewport()
    dpg.show_viewport(vp)
    dpg.set_primary_window('candlestick-chart', True)
    dpg.show_implot_demo()
    dpg.show_imgui_demo()
    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()
