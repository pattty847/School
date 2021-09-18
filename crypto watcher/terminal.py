from pycoingecko import CoinGeckoAPI
import json
import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np
from math import sin

cg = CoinGeckoAPI()

index = {
    "terminal": {
        "viewport": dpg.generate_uuid(), 
        "bitcoin": dpg.generate_uuid(), 
        "ethereum": dpg.generate_uuid(), 
        "chainlink": dpg.generate_uuid(), 
        "harmony": dpg.generate_uuid(), 
        "cardano": dpg.generate_uuid(), 
    }, 
    "chart": {
        "test": dpg.generate_uuid()
    }
}

df = pd.read_csv("BTC-USD.csv", parse_dates=True)
dates = df['Date'].to_numpy()
min_dates = min(dates)
max_dates = max(dates)
opens = df['Open'].to_numpy()
highs = df['High'].to_numpy()
max_highs = max(highs)
lows = df['Low'].to_numpy()
min_lows = min(lows)
closes = df['Close'].to_numpy()


sindatax = []
sindatay = []
for i in range(0, 100):
    sindatax.append(i/100)
    sindatay.append(0.5 + 0.5*sin(50*i/100))

# Viewport

vp = dpg.create_viewport(title='Welcome Pepe', width=1200, height=720)

with dpg.window(id = index["terminal"]['viewport'], label="Terminal"):
    dpg.add_button(id = index["terminal"]['bitcoin'], label="Bitcoin") 
    dpg.add_same_line()
    dpg.add_button(id = index["terminal"]['ethereum'], label="Ethereum") 
    dpg.add_same_line()
    dpg.add_button(id = index["terminal"]['chainlink'], label="Chainlink") 
    dpg.add_same_line()
    dpg.add_button(id = index["terminal"]['harmony'], label="Harmony") 
    dpg.add_same_line()
    dpg.add_button(id = index["terminal"]['cardano'], label="Cardano") 
    dpg.add_same_line()


    # create plot
    with dpg.plot(label="Line Series", height=400, width=400):

        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", id="y_axis")

        # series belong to a y axis
        dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")


dpg.show_item_registry()

# Setting Viewport created at top of page
dpg.setup_dearpygui(viewport=vp)
dpg.show_viewport(vp)

dpg.set_primary_window(index["terminal"]['viewport'], True)
# Render loop
dpg.start_dearpygui()