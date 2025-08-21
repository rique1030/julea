from dataclasses import dataclass
from enum import Enum


class Method(str, Enum):
    BULK = "bulk"
    SINGLE = "single"


class Command(str, Enum):
    START = "start"
    PAUSE = "pause"
    STOP = "stop"
    RESUME = "resume"

class Status(str, Enum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

class Site(str, Enum):
    GOOGLE = "google"
    NORTHDATA = "northdata"
    DNB = "dnb"
    AVOXDATA = "avoxdata"
    OPENCORPORATES = "opencorporates"
    EASYBAIDU = "easy.baidu"
    BAIKEBAIDU = "baike.baidu"
    QCCKYC = "qcckyc"

@dataclass
class AutomationCommand:
    method: Method
    command: Command

    @classmethod
    def create(cls, data):
        return cls(method=Method(data["method"]), command=Command(data["command"]))

@dataclass
class Query:
    site: list[Site]
    queries: list[str]

    @classmethod
    def create(cls, data):
        sites = [Site(s) for s in data["site"]]
        return cls(site=sites,queries=data["query"])

