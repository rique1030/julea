import dearpygui.dearpygui as dpg
import win32gui
import win32con
import win32api
import time
import os

class UserInterface():
    def __init__(self) -> None:
        # app config
        self.font_scale = 1
        self.title_bar_height = 35
        self.collapsed = False

        # app variable
        self.viewport_title = "JULEA-ignore"
        self.dragging = False
        self.drag_offset = (0,0)
        self.hwnd = None

        # initialization
        self._initialize_window()
        self._start_pygui()

    def _mouse_down_callback(self, _sender, _app_data, _user_data):
        if dpg.is_item_hovered("custom_title_bar") and dpg.is_mouse_button_down(0):
            self.dragging = True
            cx, cy = win32api.GetCursorPos()
            if self.hwnd is None:
                raise RuntimeError("HWND not initialized - window handle is None")
            wx, wy = win32gui.GetWindowRect(self.hwnd)[:2]
            self.drag_offset = (cx - wx, cy - wy)

    def _mouse_release_callback(self, _sender, _app_data, _user_data):
        self.dragging = False

    def _mouse_drag_callback(self):
        if self.hwnd is None:
            raise RuntimeError("HWND not initialized - window handle is None")
        if self.dragging and win32gui.IsWindow(self.hwnd):
            mx , my = win32api.GetCursorPos()
            dx , dy = self.drag_offset
            win32gui.SetWindowPos(self.hwnd, None, mx - dx, my - dy, 0,0, win32con.SWP_NOZORDER | win32con.SWP_NOSIZE)

    def _get_hwnd(self):
        time.sleep(0.5)
        self.hwnd = win32gui.FindWindow(None, self.viewport_title)
        
    def _change_page_callback(self, _sender, _app_data, user_data):
        self.change_page(user_data)

    def _toggle_collapse_callback(self, _sender, _app_data, _user_data):
        if not self.collapsed:
            dpg.set_viewport_height(50)
            dpg.hide_item("viewport_body")
        else:
            dpg.show_item("viewport_body")
            dpg.set_viewport_height(500)
        self.collapsed = not self.collapsed

    def change_page(self, page_id):
        dpg.hide_item("initial_page")
        dpg.hide_item("main_page")
        dpg.show_item(page_id)



    def _initialize_window(self):
        dpg.create_context()
        dpg.create_viewport(
            title=self.viewport_title,
            width=800,
            height=500,
            resizable=False,
            decorated=False,
        )
        dpg.setup_dearpygui()
        self._populate_fonts()
        self._initialize_registry()
        self._load_images()
        self._create_theme()
        self._define_main_window()
        self.change_page("initial_page")
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        self._get_hwnd()

    def _populate_fonts(self):
        font_dir = "fonts/ithaca.ttf"
        font_map = {
            "fnt_display"       : 32,
            "fnt_headline"      : 24,
            "fnt_body"          : 14,
        }
        with dpg.font_registry():
            for tag, size in font_map.items():
                with dpg.font(font_dir, size, tag=tag):
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.bind_font("fnt_body")

    def _initialize_registry(self):
        with dpg.value_registry():
            dpg.add_string_value(tag="search_method", default_value="single_mode")
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=0, callback=self._mouse_down_callback)
            dpg.add_mouse_release_handler(button=0, callback=self._mouse_release_callback)

    def _load_images(self):
        image_list = os.listdir("icons")
        with dpg.texture_registry(show=False):
            for image in image_list:
                width, height, channels, data = dpg.load_image("icons\\" + image)
                image_name = image.split(".")
                image_tag = image_name[0] + "_icon"
                dpg.add_static_texture(width, height, data, tag=image_tag)

    def _create_theme(self):
        with dpg.theme(tag="custom_bar"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30,30,30), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, ( 225,225,225), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)

    def _define_main_window(self):
        with dpg.window(tag="main_window",label="JULEA", no_scroll_with_mouse=True, no_scrollbar=True, autosize=False):
            with dpg.child_window(
                tag="custom_title_bar",
                border=False,
                height=self.title_bar_height,
            ):
                with dpg.group(horizontal=True):
                    dpg.bind_item_theme("custom_title_bar", "custom_bar")
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=5)
                        dpg.add_text("Julea: Listenning...", tag="title_bar:text")
                        dpg.bind_item_font("title_bar:text", "fnt_headline")
                        dpg.add_spacer(width=-1)
                        dpg.add_image_button(texture_tag="expand_icon", height=28, callback=self._toggle_collapse_callback)
                        dpg.add_image_button(texture_tag="close_icon", height=28)

            with dpg.group(tag="viewport_body"):
                # ----- starting window -----
                # window for displaying purpose
                with dpg.group(tag="initial_page"):
                    with dpg.child_window(tag="initial_page:body", height=380, no_scrollbar=True, no_scroll_with_mouse=True):
                        dpg.add_text("Welcome to JULEA", tag="initial_page:welcome")
                        dpg.bind_item_font("initial_page:welcome", "fnt_display")
                        dpg.add_text("Justified & Understanding Legal Entity Asistant", tag="initial_page:full_name")
                        dpg.bind_item_font("initial_page:full_name", "fnt_headline")
                    with dpg.child_window(tag="initial_page:footer", height=60, width=-1):
                        dpg.add_button(
                            label="Start Automating",
                            width=-1,
                            height=-1,
                            callback=self._change_page_callback,
                            user_data="main_page"
                        )

                # ----- main page -----
                # main page for automation

                with dpg.group(tag="main_page"):
                    with dpg.group(tag="main_page:body", horizontal=True):
                        with dpg.child_window(tag="main_page:body1",height=380,width=380):

                            # Acronym display
                            with dpg.child_window(tag="main_page:body1:title_row", width=365, height=60):
                                dpg.add_text("J.U.L.E.A", tag="main_page:acronym")
                                dpg.bind_item_font("main_page:acronym", "fnt_display")
                                
                            # Config window
                            with dpg.child_window(tag="main_page:body1:row1",width=365, height=300):
                                dpg.add_text("Select websites to search on")
                                dpg.add_checkbox(label="google")
                                with dpg.group(horizontal=True):
                                    dpg.add_input_text(readonly=True,width=275)
                                    dpg.add_button(label="Select File",width=80)

                        # OUTPUT
                        # prints output of automation search
                        with dpg.child_window(tag="main_page:body2",height=380,width=380):
                            dpg.add_text("Output")
                            dpg.add_input_text(readonly=True,
                                               width=-1,
                                               height=340,
                                               multiline=True
                                               )

                    with dpg.child_window(tag="main_page:footer"):
                        with dpg.group(horizontal=True):
                            dpg.add_text("Log: Searching for A....")
                            dpg.add_button(label="Start",width=80)
                            dpg.add_button(label="Pause",width=80)
                            dpg.add_button(label="Stop",width=80)
                        dpg.add_progress_bar(width=-1, label="scraping pogress",use_internal_label=False)

    def _start_pygui(self):
        while dpg.is_dearpygui_running():
            self._mouse_drag_callback()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()


if __name__ == "__main__":
    ui = UserInterface()
    pass

# from selenium import webdriver
# from selenium.webdriver import EdgeService, EdgeOptions
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import os
#
# # Setup Browser
# # brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#
#
# options = EdgeOptions()
# options.add_argument("--disable-logging")
# options.add_argument("--log-level=3")  # 0 = INFO, 3 = ERROR
# options.add_argument("--disable-breakpad")  # Avoid crash reports
# options.add_argument("--no-service-autorun")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--headless=new")
#
# driver = webdriver.Edge(
#     service=EdgeService(EdgeChromiumDriverManager().install()),
#     options=options
# )
#
# driver.get("https://www.google.com")
# print(driver.title)
# driver.quit()
