from typing import Callable, Any
from dearpygui import dearpygui as dpg


mouse_down_callback: Callable[[Any], None] = lambda a, b : print("Unimplemented")
mouse_release_callback: Callable[[Any], None] = lambda a, b : print("Unimplemented")

def initialize_handler(ui):
    # initialize_values(ui)
    initialize_mouse(ui)

# def initialize_values(ui):
#     with dpg.value_registry():
#         dpg.add_string_value(tag="search_method", default_value="single_mode")


def initialize_mouse(ui):
    with dpg.handler_registry():
        dpg.add_mouse_click_handler(button=0, callback=lambda s, a, u: mouse_down_callback(ui))
        dpg.add_mouse_release_handler(button=0, callback=lambda s, a, u: mouse_release_callback(ui))

