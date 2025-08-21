from seleniumbase import Driver

def create_driver(browser="edge", headless=False):
    custom_args = [
        "--disable-logging",
        "--log-level=3",  # 0 = INFO, 3 = ERROR
        "--disable-software-rasterizer",
        "--disable-breakpad",  # Avoid crash reports
        "--no-service-autorun",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--disable-dev-shm-usage",
        "--disable-blink-features",
        "--disable-features=IsolateOrigins,site-per-process",
    ]
    driver = Driver(
        uc=True,
        browser=browser,
        headless=headless,
        chromium_arg=custom_args,
        
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # driver.set_window_size(1920, 1080)

    driver.set_page_load_timeout(60)   # seconds
    # driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    #     'source': '''
    #         Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    #         Object.getOwnPropertyNames(window).filter(prop => prop.startsWith('cdc_')).forEach(prop => delete window[prop]);
    #
    #         // Override console methods that might leak automation info
    #         const noop = () => {};
    #         ['debug', 'clear', 'error', 'info', 'log', 'warn'].forEach(method => {
    #             if (typeof console[method] !== 'undefined') {
    #                 console[method] = noop;
    #             }
    #         });
    #     '''
    # })
    


    return driver


