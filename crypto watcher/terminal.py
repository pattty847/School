from pycoingecko import CoinGeckoAPI
import json
import dearpygui.dearpygui as dpg

cg = CoinGeckoAPI()
coins = cg.get_search_trending()

with dpg.window(label="main-terminal", autosize=True):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)



dpg.start_dearpygui()