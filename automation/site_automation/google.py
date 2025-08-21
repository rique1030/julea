from selenium.webdriver.common.by import By
from .qhelper import human_wait


def step_open_site(driver, query):
    driver.get("https://www.google.com/search?q=" + query)
    # human_wait()

def step_handle_captcha(driver, handle_captcha):
    return handle_captcha(driver, "google")

def step_scrape(driver, query):
    result = []
    results = driver.find_elements(By.CSS_SELECTOR, '[jsname="UWckNb"]')
    try:  
        for bresult in results:
            try:
                title_element = bresult.find_element(By.TAG_NAME, "h3")
                link = bresult.get_attribute("href")
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
    step_scrape
]

def get_steps():
    return steps

def get_args(driver, query, handler_captcha):
    return [
        (driver, query),
        (driver, handler_captcha),
        (driver, query),
    ]

