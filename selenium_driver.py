from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver_by_system():
    import platform

    if platform.system() == 'Windows':
        print('当前系统为 Windows')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        #options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        #options.add_argument('--disable-gpu')
        return webdriver.Firefox(options=options)
    elif platform.system() == 'Linux':
        print('当前系统为 Linux')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return webdriver.Firefox(options=options)
    elif platform.system() == 'Darwin':
        print('当前系统为 macOS')
        # 设置浏览器选项
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return webdriver.Chrome(options=options)
    else:
        print('无法确定当前系统类型')
        return None

def get_driver(implicitly_wait=10,page_load_timeout=15):
    driver = get_driver_by_system()
    if(driver is None):
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=options)
    # 设置最大等待时间为10秒
    driver.implicitly_wait(implicitly_wait)
    driver.set_page_load_timeout(page_load_timeout)
    return driver