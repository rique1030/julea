from selenium.webdriver.common.by import By
from .qhelper import wait_for_page_load



def step_open_site(driver):
    driver.get("https://www.avoxdata.com")

def step_handle_captcha(driver, handle_captcha):
    return handle_captcha(driver, "avoxdata")

def step_search(driver, query):
    search_bar = driver.find_element(By.ID, "entity-search")
    search_bar.send_keys(query)
    search_bar.submit()
    wait_for_page_load(driver)

def step_scrape(driver):

    rows = driver.find_elements(By.CSS_SELECTOR, "tr")
    result = []
    try:
        for row in rows :
            try:
                first_cell = driver.execute_script("return arguments[0].firstElementChild", row)
                title_element = first_cell.find_element(By.TAG_NAME, "a")
                link = title_element.get_attribute("href")
                title = title_element.text.strip()

                if title and link:
                    result.append({
                        "title": title,
                        "link": link
                        })
            except Exception as e:
                print(f"{e}")
    except Exception as e:
        print(f"{e}")
    finally:
        return result



steps = [
    step_open_site,
    step_handle_captcha,
    step_search,
    step_scrape
]

def get_steps():
    return steps

def get_args(driver, query, handler_captcha):
    return [
        (driver,),
        (driver, handler_captcha),
        (driver, query),
        (driver,)
    ]

