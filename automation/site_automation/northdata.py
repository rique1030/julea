from typing import List
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .qhelper import wait_for_page_load

def step_open(driver, query):
    query = query.replace(" ", "+")
    driver.get("https://www.northdata.com/" + query)
    wait_for_page_load(driver)

def step_handle_captcha(driver, handle_captcha):
    try:
        driver.find_element(By.ID, "cmpwelcomebtnyes").click()
    except Exception as e:
        print(f"{e}")
    return handle_captcha(driver, "northdata")

def step_scrape(driver):
    result = []
    try:
        broad_result = broad_search(driver)
        for bresult in broad_result:
            result.append({
                "title": bresult[0],
                "link": bresult[1]
            })
        return result
    except NoSuchElementException:
        try:
            title = direct_search(driver)
            result.append({
                "title": title,
                "link": driver.current_url
            })
        except NoSuchElementException as e:
            print(f"{e}")
    except Exception as e:
        print(f"{e}")
    finally:
        return result


steps = [
    step_open,
    step_handle_captcha,
    step_scrape
]

def get_steps():
    return steps

def get_args(driver, query, handle_captcha):
    return [
        (driver, query),
        (driver, handle_captcha),
        (driver,)
    ]

def broad_search(driver) -> List[str]:
    sites = []
    wrapper = driver.find_element(By.CLASS_NAME, "column")
    content_feed = wrapper.find_element(By.CSS_SELECTOR, ".ui.feed")
    contents = content_feed.find_elements(By.CLASS_NAME, "event")

    for content in contents:
        title_element = content.find_element(By.TAG_NAME, "a")
        link = title_element.get_attribute("href")
        title = title_element.text.strip()
        if title and link:
            sites.append((title, link))
    return sites

def direct_search(driver):
    wrapper = driver.find_element(By.CSS_SELECTOR, ".ui.header.large.qualified")
    title = wrapper.find_element(By.CLASS_NAME, "heading").text
    return title
