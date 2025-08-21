from time import sleep
from random import uniform
from selenium.webdriver.support.ui import WebDriverWait

def human_wait( base=2.5, variance=1.5):
    sleep(base + uniform(0, variance))

def wait_for_page_load(driver):
    return WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

