import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg
from pycoingecko import CoinGeckoAPI



cg = CoinGeckoAPI()

# Main program viewport
vp = dpg.create_viewport(title='TradeSuite', width=1600, height=1200)
dpg.setup_dearpygui(viewport=vp)


def save_callback():
    print("Save Clicked")

def get_input(sender, app_data, user_data):
    dpg.set_value('results', cg.get_price(dpg.get_value('input'), vs_currencies='usd'))

# TradeSuite homepage
def start_viewport():
    with dpg.window(id = "candlestick-chart", label="TradeSuite", width=500, height=500):
        dpg.add_input_text(id="input", label='Enter a Crypto')
        dpg.add_button(label="Search Coin Price", callback=get_input)
        dpg.add_text(id='results')
        dpg.add_table()

        




if(__name__ == "__main__"):
    start_viewport()
    dpg.show_viewport(vp)
    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()