from selenium.webdriver.common.by import By
from seleniumbase.core.sb_driver import WebDriver
from .qhelper import human_wait, wait_for_page_load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

def step_open_site(driver):
    driver.get("https://www.qcckyc.com")
    human_wait()

def step_zoom(driver):
    driver.execute_script("document.body.style.zoom='67%'")

def step_handle_captcha(driver, handle_captcha):
    handle_captcha(driver, "qcckyc")
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-button.g-button.accept-cookie-btn.font-weight-bold.el-button--primary.el-button--small.is-round"))
        )
        buttons[1].click()
    except Exception as e:
        print(f"{e}")
    wait_for_page_load(driver)
    human_wait()

def step_navigate_to_search(driver):
    button_container = driver.find_element(By.CLASS_NAME, "layout-header-right")
    buttons = button_container.find_elements(By.TAG_NAME, "button")
    buttons[0].click()
    human_wait()


def step_search(driver, query):
    search_bar = driver.find_element(By.CLASS_NAME, "comp-search-input")
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.ENTER)

def step_scrape(driver):
    items = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ssr-kyc-search-company__name"))
    )
    driver.execute_script("""
      window._detail_url = null;
      window.open = function(url, name, specs) {
        window._detail_url = url;
        // return a dummy Window-like object so page scripts don’t crash
        return { closed: false, close: function() {}, focus: function() {} };
      };
    """)
    result = []
    try:
        for item in items:
            spans = item.find_elements(By.TAG_NAME, "span")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
            title = spans[0].text
            driver.execute_script("window._detail_url = null;")
            # item.click()
            human_wait(0.2)
            # item.click()
            spans[0].click()
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return window._detail_url;") is not None
            )
            link = driver.execute_script("return window._detail_url;")

            human_wait(0.2)
            if title and link:
                result.append({
                    "title": title,
                    "link": link
                })
    except Exception as e:
        print(f"{e}")
    finally:
        return result



steps = [
    step_open_site,
    step_zoom,
    step_handle_captcha,
    step_navigate_to_search,
    step_search,
    step_scrape
]


def get_steps():
    return steps

def get_args(driver, query, handle_captcha):
    return [
        (driver,),
        (driver,),
        (driver, handle_captcha),
        (driver,),
        (driver, query),
        (driver,)
    ]
