from dearpygui import dearpygui as dpg
import os

def load_assets():
    load_images()
    load_fonts()

def load_images():
    images = os.listdir("icons")
    with dpg.texture_registry(show=False):
        for image in images:
            width, height, channels, data = dpg.load_image("icons\\" + image)
            image_name = image.split(".")
            image_tag = image_name[0] + "_icon"
            dpg.add_static_texture(width, height, data, tag=image_tag)

def load_fonts():
    font_dir = "fonts/Consolas.ttf"
    default_size = 14.0
    font_map = {
        "fnt_display"       : 2.0,
        "fnt_headline"      : 1.5,
        # "fnt_title"         : 1.3,
        "fnt_body"          : 1.0,
    }
    with dpg.font_registry():
        for tag, size in font_map.items():
            with dpg.font(font_dir, int(size * default_size), tag=tag):
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.bind_font("fnt_body")
