from dearpygui import dearpygui as dpg

from ui import registry, tags
from . import configuration, components, loaders, handlers, window, logger

class UserInterface:
    def __init__(self) -> None:
        # app config
        self.font_scale: float = 1.0
        self.title_bar_height: int = 35
        self.viewport_title: str = configuration.VIEWPORT_TITLE

        # websites
        self.websites = {
            "chinese": [
                "easy.baidu.com",
                "baike.baidu.com",
                "qcckyc.com"
            ],
            "euro/american": [
                "northdata.com",
                "avoxdata.com",
                "opencorporates.com",
                "dnb.com",
            ],
            "shared" : [
                "google.com"
            ]
        }

        # app states
        self.dragging: bool = False
        self.current_page: str = tags.WELCOME_PAGE_TAG
        self.is_search_batch = True
        self.collapsed = False

        self.initialize_window()
        self.start_pygui()


    def assign_callbacks(self):
        logger.info("Assigning callbacks...")
        components.on_btn_next_page = handlers.change_page_callback
        components.on_checkbox_batch_check = handlers.toggle_search_mode
        components.on_btn_close = handlers.on_window_close
        components.on_btn_collapse = handlers.on_window_collapse

        registry.mouse_down_callback = handlers.mouse_down_callback
        registry.mouse_release_callback = handlers.mouse_release_callback

        
    def initialize_window(self):
        logger.info("Initializing window...")
        dpg.create_context()
        dpg.create_viewport(
            title=self.viewport_title,
            width=800,
            height=500,
            resizable=False,
            decorated=False
        )
        dpg.setup_dearpygui()
        # start here
        self.assign_callbacks()
        loaders.load_assets()
        components.create_window(self)
        handlers.change_page_callback(self, tags.WELCOME_PAGE_TAG)
        handlers.toggle_search_mode(self)
        # end
        dpg.show_viewport()
        window.get_window_frame(self)
        registry.initialize_handler(self)

    def start_pygui(self):
        logger.info("Starting pygui...")
        while dpg.is_dearpygui_running():
            handlers.on_mouse_drag(self)
            dpg.render_dearpygui_frame()
        dpg.destroy_context()


