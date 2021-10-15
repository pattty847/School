import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg
from pycoingecko import CoinGeckoAPI
from pprint import pprint
import pandas as pd
import datetime


cg = CoinGeckoAPI()

# Main program viewport
vp = dpg.create_viewport(title='TradeSuite', width=1600, height=1200)
dpg.setup_dearpygui(viewport=vp)


def getOHLC(sender, app_data, user_data):

    btc_OHLC = cg.get_coin_ohlc_by_id(dpg.get_value('input'), vs_currency='usd', days=90)
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

# TradeSuite homepage
def start_viewport():
    with dpg.window(id = "candlestick-chart", label="TradeSuite"):
        dpg.add_input_text(id="input", label='Enter a Crypto')
        dpg.add_button(label="Search Coin Price", callback=getOHLC)
        dpg.add_table(id='results')
        

        



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
