from selenium.webdriver.common.by import By
from .qhelper import human_wait, wait_for_page_load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

def step_open_site(driver, query):
    query = query.replace(" ", "+")
    driver.get("https://www.baidu.com/s?wd=" + query)
    human_wait()

def step_handle_captcha(driver, handle_captcha):
    return handle_captcha(driver, "easy_baidu")

def step_scrape(driver):
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content_left"))
    )

    contents = container.find_elements(By.CSS_SELECTOR,'div[class^="title-wrapper_"]')
    
    result = []
    for content in contents:
        title_element = content.find_element(By.TAG_NAME, "a")
        link = title_element.get_attribute("href")
        title = title_element.text.strip()
        if title and link:
            result.append({
                "title": title,
                "link": link
            })
    return result

steps = [
    step_open_site,
    step_handle_captcha,
    step_scrape
]

def get_steps():
    return steps

def get_args(driver, query, handler_captcha):
    return [
        (driver,query),
        (driver, handler_captcha),
        (driver,)
    ]
