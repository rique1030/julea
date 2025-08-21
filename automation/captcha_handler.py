from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import time, sleep
from .appconfig import config
import pickle
import os

def check_for_captcha(driver, site,  timeout = 120):
    try:
        driver.find_element(By.ID, "rc-anchor-container")
    except NoSuchElementException:
        return True
    return False


def save_cookies(driver, domain):
    with open(os.path.join(config.JULEA_PATH, 'cookies', f"{domain}.pkl"), 'wb') as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookies(driver, domain):
    path = os.path.join(config.JULEA_PATH, 'cookies', f"{domain}.pkl")
    if not os.path.isfile(path):
        # print("Cookie file not found")
        return False
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        return True


def handle_captcha(driver, domain) -> bool:
    if load_cookies(driver, domain):
        driver.refresh()
    return check_for_captcha(driver, domain)
