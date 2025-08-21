from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .qhelper import human_wait, wait_for_page_load
from selenium.webdriver.common.keys import Keys


def step_inject_script(driver):
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.getOwnPropertyNames(window).filter(prop => prop.startsWith('cdc_')).forEach(prop => delete window[prop]);
            
            // Override console methods that might leak automation info
            const noop = () => {};
            ['debug', 'clear', 'error', 'info', 'log', 'warn'].forEach(method => {
                if (typeof console[method] !== 'undefined') {
                    console[method] = noop;
                }
            });
        '''
    })

def step_open_site(driver):
    driver.get("https://easy.baidu.com/")
    human_wait()

def step_handle_captcha(driver, handle_captcha):
    handle_captcha(driver, "easy_baidu")
    human_wait()

def step_search(driver, query):
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "aqc-search-input"))
    )
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.ENTER)
    wait_for_page_load(driver)

def step_scrape(driver):
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "list-wrap"
                    )
                )
        )

        cards = container.find_elements(By.CLASS_NAME, "card")
        result = []
        for card in cards:
            title_element_container = card.find_element(By.CLASS_NAME, "title")
            title_element = title_element_container.find_element(By.TAG_NAME, "a")
            data_id = title_element.get_attribute("data-log-title")
            if data_id is None:
                continue
            data_id = data_id.split("item-")[1]        
            link = f"https://easy.baidu.com/company_detail_{data_id}"
            title = title_element.text.strip()
            if title and link:
                result.append({
                    "title": title,
                    "link": link
                })
    except Exception as e:
        print(f"{e}")
    finally:
        restore_automation_properties(driver)
        return result

steps = [
    step_inject_script,
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
        (driver,),
        (driver, handle_captcha),
        (driver, query),
        (driver,)
    ]

def restore_automation_properties(driver):
    """Restore automation properties for sites that expect them"""
    # Clear the stealth script for future pages
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            // Restore webdriver property
            Object.defineProperty(navigator, 'webdriver', {get: () => true});
            
            // Restore common CDC properties with typical patterns
            window.cdc_adoQpoasnfa76pfcZLmcfl_Array = Array;
            window.cdc_adoQpoasnfa76pfcZLmcfl_Promise = Promise;
            window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol = Symbol;
            window.cdc_adoQpoasnfa76pfcZLmcfl_Object = Object;
            
            // Restore console methods
            ['debug', 'clear', 'error', 'info', 'log', 'warn'].forEach(method => {
                if (typeof console[method] === 'undefined' || console[method].toString() === '() => {}') {
                    console[method] = console.info; // Restore to working function
                }
            });
        '''
    })
