from dearpygui import dearpygui as dpg
from . import tags, logger, tags
import win32gui
import win32api
import win32con

def mouse_down_callback(ui):
    if dpg.is_item_hovered(tags.TITLE_BAR_TAG) and dpg.is_mouse_button_down(0):
        logger.info("Titlebar mouses down...")
        ui.dragging = True
        cx, cy = win32api.GetCursorPos()
        if ui.hwnd is None:
            raise RuntimeError("HWND not initialized - window handle is None")
        wx, wy = win32gui.GetWindowRect(ui.hwnd)[:2]
        ui.drag_offset = (cx - wx, cy - wy)

def mouse_release_callback(ui):
    if ui.dragging == False: return
    logger.info("Titlebar mouse release...")
    ui.dragging = False

def on_mouse_drag(ui):
    if ui.hwnd is None:
        raise RuntimeError("HWND not initialized - window handle is None")
    if ui.dragging and win32gui.IsWindow(ui.hwnd):
        mx , my = win32api.GetCursorPos()
        dx , dy = ui.drag_offset

        logger.debug(f"Mouse dragging... {mx} {my} {dx} {dy}")
        win32gui.SetWindowPos(ui.hwnd, None, mx - dx, my - dy, 0,0, win32con.SWP_NOZORDER | win32con.SWP_NOSIZE)
    
def change_page_callback(ui, page_tag: str) -> None:
    logger.info(f"Changing page to {page_tag}")
    dpg.hide_item(tags.WELCOME_PAGE_TAG)
    dpg.hide_item(tags.MAIN_PAGE_TAG)
    dpg.show_item(page_tag)
    ui.current_page = page_tag




def toggle_search_mode(ui):
    ui.is_search_batch = not ui.is_search_batch
    dpg.hide_item(tags.MAIN_PAGE_SINGLE_INPUT_TAG)
    dpg.hide_item(tags.MAIN_PAGE_BATCH_INPUT_TAG)
    page_to_show = tags.MAIN_PAGE_BATCH_INPUT_TAG if ui.is_search_batch else tags.MAIN_PAGE_SINGLE_INPUT_TAG
    dpg.show_item(page_to_show)


def on_window_close() -> None:
    logger.info("Window close...")
    dpg.stop_dearpygui()

def on_window_collapse(ui) -> None:
    logger.info("Window collapse...")
    if not dpg.does_item_exist(tags.MAIN_WINDOW_TAG):
        raise RuntimeError("Viewport body does not exist")

    if not ui.collapsed:
        dpg.set_viewport_height(40)
        dpg.set_viewport_width(400)
        # dpg.set_item_height(tags.MAIN_WINDOW_TAG, height=50)
        dpg.hide_item(ui.current_page)
    else:
        dpg.show_item(ui.current_page)
        dpg.set_viewport_width(800)
        dpg.set_viewport_height(500)
    ui.collapsed = not ui.collapsed
