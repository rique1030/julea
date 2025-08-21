from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .qhelper import wait_for_page_load, human_wait


def step_open_site(driver):
    driver.get("https://www.opencorporates.com")
    wait_for_page_load(driver)


def step_handle_captcha(driver, handle_captcha):
    handle_captcha(driver, "opencorporates")
    wait_for_page_load(driver)
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cky-btn.cky-btn-accept"))
        )
        accept_button.click()
        human_wait()
    except:
        pass

def step_search(driver, query):
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", search_bar)
    human_wait()
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.submit()
    wait_for_page_load(driver)
    human_wait()

def step_scrape(driver):
    result = []
    try:
        companies = driver.find_elements(By.CSS_SELECTOR, ".search-result")
        for company in companies:
            try:
                title_element = company.find_element(By.CSS_SELECTOR, ".company_search_result")
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


def get_args(driver, query, handle_captcha):
    return [
        (driver,),
        (driver, handle_captcha),
        (driver, query),
        (driver,)
    ]
