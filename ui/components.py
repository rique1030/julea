from typing import Callable, Any
from dearpygui import dearpygui as dpg
from . import tags, logger


on_btn_next_page: Callable[[Any, str], None] = lambda a, b: logger.debug("Callback unimplemented")
on_checkbox_batch_check: Callable[[Any], None] = lambda a: logger.debug("Callback unimplemented")


on_btn_close: Callable[[], None] = lambda : logger.debug("Callback unimplemented")
on_btn_collapse: Callable[[Any], None] = lambda a: logger.debug("Callback unimplemented")


on_process_control : Callable[[Any], None] = lambda a: logger.debug("Callback unimplemented")

def create_window(ui):
    logger.info("Creating window...")
    with dpg.window(tag=tags.MAIN_WINDOW_TAG, height=-1):
        dpg.set_primary_window(tags.MAIN_WINDOW_TAG, True)
        title_bar(ui)
        welcome_page(ui)
        main_page(ui)

def title_bar(ui):
    with dpg.group(horizontal=True):
        with dpg.child_window(
            tag=tags.TITLE_BAR_TAG,
            border=False,
            height=28,
            width=-72
        ):
            dpg.add_text("Julea: At your service", tag=tags.TITLE_BAR_TEXT_TAG)
            dpg.bind_item_font(tags.TITLE_BAR_TEXT_TAG, "fnt_headline")
        dpg.add_image_button(texture_tag=tags.EXPAND_TEXTURE_TAG, height=20, width=20, callback=lambda : on_btn_collapse(ui))
        dpg.add_image_button(texture_tag=tags.CLOSE_TEXTURE_TAG, height=20, width=20, callback=on_btn_close)


def welcome_page(ui):
    logger.info("Creating welcome page...")
    with dpg.group(tag=tags.WELCOME_PAGE_TAG):
        with dpg.child_window(height=-70):
            with dpg.group(horizontal=True):
                with dpg.child_window(border=False, width=-350):

                    welcome_page_title()
                    dpg.add_spacer(height=25)
                    welcome_page_features()
                    dpg.add_spacer(height=25)
                    dpg.add_text("This is a technical tool. Results are for reference only")
                    dpg.add_text("and not leaglly binding")


                with dpg.child_window(border=False, width=-10):
                    dpg.add_spacer(height=25)
                    dpg.add_image(texture_tag=tags.JULEA_TEXTURE_TAG, height=300, width=300)

        welcome_page_controls(ui)


def welcome_page_title():
    dpg.add_text("Welcome to JULEA", tag=tags.WELCOME_PAGE_GREETING_TAG)
    dpg.bind_item_font(tags.WELCOME_PAGE_GREETING_TAG, "fnt_display")

    dpg.add_spacer(height=5)

    dpg.add_text("Justified & Understanding Legal", tag=tags.WELCOME_PAGE_ACRONYM1_TAG)
    dpg.add_text("Entity Asistant", tag=tags.WELCOME_PAGE_ACRONYM2_TAG)
    dpg.bind_item_font(tags.WELCOME_PAGE_ACRONYM1_TAG, "fnt_headline")
    dpg.bind_item_font(tags.WELCOME_PAGE_ACRONYM2_TAG, "fnt_headline")


def welcome_page_features():
    dpg.add_text("Key Features:", tag=tags.WELCOME_PAGE_FEATURE_TITLE_TAG)
    dpg.bind_item_font(tags.WELCOME_PAGE_FEATURE_TITLE_TAG, "fnt_title")
    dpg.add_text("- Scrapes different hardcoded sites")
    dpg.add_text("- Quick company existence check")
    dpg.add_text("- Raw results, no guessing")


def welcome_page_controls(ui):
    with dpg.child_window(tag=tags.WELCOME_PAGE_FOOTER_TAG, height=60, width=-1):
        dpg.add_button(
            label="Start Automating",
            width=-1,
            user_data=tags.MAIN_PAGE_TAG,
            callback=lambda s, a, u: on_btn_next_page(ui, u),
            height=-1,
        )


def main_page(ui):
    logger.info("Creating main page...")
    with dpg.group(tag=tags.MAIN_PAGE_TAG):
        with dpg.group(horizontal=True):
            main_page_input(ui)
            main_page_output(ui)
        main_page_controls(ui)


def main_page_input(ui):
    with dpg.child_window(width=400, height=-75):

        dpg.add_text("Website Selection")
        dpg.add_spacer(height=5)
        with dpg.collapsing_header(label="Chinese Websites"):
            for site in ui.websites["chinese"]:
                dpg.add_checkbox(label=site)

        with dpg.collapsing_header(label="European/American Websites"):
            for site in ui.websites["euro/american"]:
                dpg.add_checkbox(label=site)
                
        with dpg.collapsing_header(label="Shaed Websites"):
            for site in ui.websites["shared"]:
                dpg.add_checkbox(label=site)

        dpg.add_spacer(height=5)
        dpg.add_separator()

        dpg.add_text("Search Method")
        dpg.add_spacer(height=5)
        dpg.add_checkbox(label="Batch Searching", callback=lambda: on_checkbox_batch_check(ui))
        dpg.add_spacer(height=5)

        with dpg.group(tag=tags.MAIN_PAGE_BATCH_INPUT_TAG):
            dpg.add_text("Select a text file containing the company names")
            with dpg.group(horizontal=True):
                dpg.add_input_text(readonly=True, width=-100)
                dpg.add_button(label="Select",width=-1)

        with dpg.group(tag=tags.MAIN_PAGE_SINGLE_INPUT_TAG):
            dpg.add_text("Enter a company name")
            dpg.add_input_text(width=-1)

def main_page_output(ui):
    with dpg.child_window(width=-1, height=-75):
        dpg.add_text("Output")
        dpg.add_checkbox(label="Open sites in Browser")
        dpg.add_input_text(
            readonly=True,
           width=-1,
           height=-1,
           multiline=True
           )


def main_page_controls(ui):
    with dpg.child_window(width=-1):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=-110, height=30, border=False):
                dpg.add_text("Log: Searching for A....")
            dpg.add_image_button(texture_tag=tags.START_TEXTURE_TAG, height=20, width=20, callback=on_process_control)
            dpg.add_image_button(texture_tag=tags.PAUSE_TEXTURE_TAG, height=20, width=20, callback=on_process_control)
            dpg.add_image_button(texture_tag=tags.STOP_TEXTURE_TAG, height=20, width=20, callback=on_process_control)
        dpg.add_progress_bar(width=-1, label="scraping pogress",use_internal_label=False)


