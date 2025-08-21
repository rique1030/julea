from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .qhelper import human_wait, wait_for_page_load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def step_open_site(driver):
    driver.get("https://www.dnb.com")
    human_wait()

def step_zoom(driver):
    driver.execute_script("document.body.style.zoom='67%'")

def step_handle_captcha(driver, handle_captcha):
    try:
        button_container = driver.find_element(
                By.ID,
                "truste-consent-button"
            )
        button_container.click()
    except NoSuchElementException:
        print("accept cookies button not found")
    except Exception as e:
        print(f"{e}")
    handle_captcha(driver, "northdata")
    pass

def step_navigate_to_business_dir(driver):
    search_options = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[aria-label='Search Options']"
                    )
                )
            )
    search_options.click()

    human_wait(base=0.5)

    button_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@aria-label='Search Options']/following-sibling::*[1]"
                )
            )
    )

    button_container = button_container.find_elements(By.TAG_NAME, "a")
    for button in button_container:
        if button.text == "Business Directory":
            button.click()
            break

    wait_for_page_load(driver)

def step_search(driver, query):
    search_bars = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
    )

    for el in search_bars:
        if el.is_displayed() and el.is_enabled():
            driver.execute_script("arguments[0].scrollIntoView();", el)
            el.clear()
            el.send_keys(query)
            el.send_keys(Keys.RETURN)
            break

    wait_for_page_load(driver)
    human_wait(0.5)

def step_scrape(driver):
    rows = driver.find_elements(By.TAG_NAME, "tr")
    result = []
    try:
        for row in rows:
            try:
                first_child = driver.execute_script("return arguments[0].firstElementChild", row)
                if not first_child: continue

                title_element = first_child.find_element(By.TAG_NAME, "a")
                title = title_element.text.strip()
                link = title_element.get_attribute("href")
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
    step_zoom,
    step_handle_captcha,
    step_navigate_to_business_dir,
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
        (driver,),
    ]
