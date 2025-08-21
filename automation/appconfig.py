import os

class AppConfig:
    def __init__(self) -> None:
        self.DOCUMENTS_PATH = os.path.join(os.environ['USERPROFILE'],"Documents")
        self.JULEA_PATH = os.path.join(self.DOCUMENTS_PATH,"Julea")
        self.DRIVER_PATH = os.path.join(self.JULEA_PATH,"drivers")
        self.BROWSERS = ['brave', 'chrome', 'edge', 'firefox' ]

config = AppConfig()
