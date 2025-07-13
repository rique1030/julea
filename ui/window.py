import win32gui
import time
from . import configuration

def get_window_frame(ui):
    time.sleep(0.5)
    ui.hwnd = win32gui.FindWindow(None, configuration.VIEWPORT_TITLE)
