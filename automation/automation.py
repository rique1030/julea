import json
import webbrowser
import webview
import os
from time import time
from typing import cast
from . import config_manager, driver_manager, captcha_handler
from .site_automation import google, northdata, dnb,avoxdata, opencorporates, easy_baidu, baike_baidu,qcckyc
from .appconfig import config
from .custom_types import AutomationCommand, Query, Command, Status, Site

class Automation:
    def __init__(self) -> None:
        self.create_directory()
        self.status = Status.STOPPED
        self.loader_value = 0.0
        self.increment = 0.0
        self.current_function = ""
        self.current_site = ""
        self.headless = False
        self.scripts = {
            "google": google,
            "northdata": northdata,
            "dnb": dnb,
            "avoxdata": avoxdata,
            "opencorporates": opencorporates,
            "easy.baidu": easy_baidu,
            "baike.baidu": baike_baidu,
            "qcckyc": qcckyc
        }

        self.commands = {
            Command.START.value: self.start_automation,
            Command.PAUSE.value: self.pause_automation,
            Command.RESUME.value: self.resume_automation,
            Command.STOP.value: self.stop_automation

        }

        self.current_request: Query = Query.create({
            "site": [],
            "query": []

        })

    def open_in_browser(self, url):
        webbrowser.open(url)
        return True

    def get_status(self):
        return self.status


    def is_driver_alive(self) -> bool:
        try:
            self.driver.title
            return True
        except:
            return False

    def handle_request(self, payload):
        try:
            query = payload.get("query", {})
            cmd = payload.get("cmd", {})
            self.headless = payload.get("headless", False)
            self.create_query(query)
            return self.send_command(cmd)
        except Exception as e:
            print(f"{e}")


    def create_query(self, payload):
        try:
            data = Query.create(payload)
            self.current_request = data
        except Exception as e:
            print(f"{e}")

    
    def send_command(self, payload):
        try:
            data = AutomationCommand.create(payload)
            command = self.commands.get(data.command.value)
            if command: 
                return command()
            else: 
                return {}
        except Exception as e:
            print(f"{e}")

    def start_automation(self):
        assert not self.is_driver_alive(), "A driver process is still running, Pleae wait a moment."
        assert self.status == Status.STOPPED, "A process is still running."
        self.status = Status.RUNNING
        try:
            browser = config_manager.get_default_browser()
            self.driver = driver_manager.create_driver(browser, self.headless)
            self.get_load(self.current_request)
            result = self.scrape(self.current_request)
            self.loader_value = 1.0 - self.increment
            self.current_function = "step_scraping_complete"
        except Exception as e:
            self.current_function = "step_something_went_wrong"
            print(f"{e}")
            self.update_load()
        finally:
            self.status = Status.STOPPED
            self.current_site = ""
            self.driver.quit()
            self.update_load()
        return result
        
    def pause_automation(self):
        assert self.is_driver_alive(), "Process should be running to pause."
        assert self.status == Status.RUNNING, "Process should be running to pause."
        self.status = Status.PAUSED

    def resume_automation(self):
        assert self.is_driver_alive(), "Process should exist and paused to resume."
        assert self.status == Status.PAUSED, "Process should be paused to resume."
        self.status = Status.RUNNING
    
    def stop_automation(self):
        assert self.is_driver_alive(), "Process should exist to stop."
        assert self.status != Status.STOPPED, "Process should be running to stop."
        self.status = Status.STOPPED
        self.driver.quit()

    def get_load(self, query: Query):
        self.loader_value = 0.0
        total_load  = 0
        for qry in query.queries:
            for site in query.site:
                total_load += len(self.scripts[site.value].get_steps())
        total_load += 1
        self.increment = 1.0 / total_load

    def update_load(self):
        self.loader_value += self.increment
        func = self.current_function.split("_")
        func.pop(0)
        for i in range(len(func)):
            func[i] = func[i].capitalize()
        func = " ".join(func)
        print(f"{self.current_site.upper()} {self.status.value.upper()} - {func} {(self.loader_value * 100):.2f}%")
        payload = {
                "site": self.current_site,
                "progress_value": self.loader_value,
                "process_info": func,
                "status": self.status
                }
        try:
            webview.windows[0].evaluate_js(f"window.setCurrentProgress({json.dumps(payload)})")
        except Exception as e:
            print(f"{e}")
        return (self.loader_value, func)

    def scrape(self, query: Query):
        general_result = {}
        sites = self.sort_sites(query.site)
        search_queries = query.queries
    
        for qry in search_queries:
            tmp_query_result = {}
            for i, site in enumerate(sites):
                self.current_site = site
                while self.status == Status.PAUSED:
                    time.sleep(1)
                if self.status == Status.STOPPED:
                    break
                tmp_result = {
                        "results": [],
                        "error": None
                    }
                try:
                    if i > 0:
                        self.driver.switch_to.new_window("tab")
                    site_args = self.scripts[site.value].get_args(
                            self.driver,
                            qry,
                            captcha_handler.handle_captcha
                            )
                    site_steps = self.scripts[site.value].get_steps()
                    tmp_result["results"] = self.search_loop( site_args, site_steps)
                except Exception as e:
                    print(f"{site} failed with {e}")
                    tmp_result["error"] = str(e.__class__)

                tmp_query_result[site.value] = tmp_result

            general_result[qry] = tmp_query_result

        return general_result

    def search_loop(self, args, steps):
        result = []
        for func, args in zip(steps, args):
            self.current_function = func.__name__
            name = self.update_load()
            result = func(*args)
            if name == "Handle Captcha":
                if result == True:
                    self.status = Status.PAUSED
        return result

    def create_directory(self):
        try:
            for browser in config.BROWSERS:
                if not os.path.exists(f"{config.DRIVER_PATH}\\{browser}"):
                    os.makedirs(f"{config.DRIVER_PATH}\\{browser}")
            if not os.path.exists(f"{config.JULEA_PATH}\\cookies"):
                os.makedirs(f"{config.JULEA_PATH}\\cookies")
        except Exception as e:
            print(f"{e}")

    def sort_sites(self,sites: list[Site]) -> list[Site]:
        site_array = [site for site in sites]
        if Site.DNB in sites:
            site_array.insert(0, site_array.pop(site_array.index(Site.DNB)))
        if Site.EASYBAIDU in sites:
            site_array.insert(0, site_array.pop(site_array.index(Site.EASYBAIDU)))
        return site_array


