import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

def get_keywords(count):
    if(count==None):
        count=10
    movies=pd.read_csv('data/input.csv',encoding='utf-8')
    return movies.Title.values

def get_driver_options():
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
        return options
    elif platform.system() == 'Linux':
        print('当前系统为 Linux')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return options
    elif platform.system() == 'Darwin':
        print('当前系统为 macOS')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return options
    else:
        print('无法确定当前系统类型')
        return None

def get_driver():
    driver = webdriver.Firefox(options=get_driver_options())
    return driver

def search(driver,keyword):
    print("search:",keyword)
    # 在搜索框中输入关键词并提交搜索
    search_box = driver.find_element(By.CLASS_NAME,"imdb-header-search__input")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # 等待搜索结果页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item")))

    # 获取搜索结果中第一个电影的链接
    first_result = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
    print(first_result)
    print(len(first_result))
    if(len(first_result)>0):
        links=first_result[0].find_elements(By.TAG_NAME,'a')
        if(len(links)>0):
            link=links[0]
            movie_url = link.get_attribute("href")
            print("movie Title:",keyword, movie_url)
            return {"Title":keyword,"url":movie_url,'time':datetime.datetime.now()}

def main():
    driver = get_driver()
    # 打开IMDB网站
    driver.get("https://www.imdb.com/")
    csv_file='data/output.csv'
    datas=[]
    for keyword in get_keywords(10):
        try:
            result=search(driver=driver,keyword=keyword)
            if(result is not None):
                datas.append(result)
            df = pd.DataFrame(result, columns=['Title','url','time'])
            try:
                csv_df=pd.read_csv(csv_file,index=False)
                csv_df.merge(df)
                csv_df.drop_duplicates(subset=['link'],keep='last',inplace=True)
                csv_df.to_csv(csv_file)
                print("csv 合并成功",flush=True)
            except:
                df.to_csv(csv_file,index=False)
                print("csv 新建成功",flush=True)
        except Exception as e:
            # 关闭浏览器
            driver.quit()
            driver = get_driver()
            # 打开IMDB网站
            driver.get("https://www.imdb.com/")
    return csv_file