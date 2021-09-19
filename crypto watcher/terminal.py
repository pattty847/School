import dearpygui.dearpygui as dpg
import pandas as pd



class Terminal():

    vp = dpg.create_viewport(title = "Window", height=700, width=1200)

    def __init__(self):
        pass

    def create_window():
        with dpg.window(id = "Main Window", label="Terminal"):
            pass

    dpg.show_item_registry()

    # Setting Viewport created at top of page
    dpg.setup_dearpygui(viewport=vp)
    dpg.show_viewport(vp)

    dpg.set_primary_window("Main Window", True)
    # Render loop
    dpg.start_dearpygui()