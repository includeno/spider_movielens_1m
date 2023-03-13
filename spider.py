import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from tqdm import tqdm
import time

def get_keywords(index,limit=None):
    movies=pd.read_csv(f'data/input_{index}.csv',encoding='utf-8')
    if(limit==None):
        return movies.Title.values
    return movies.Title.values[:limit]

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

def get_driver():
    driver = get_driver_by_system()
    if(driver is None):
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=options)
    # 设置最大等待时间为10秒
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(15)
    return driver

def search(driver,keyword):
    print("search:",keyword,flush=True)
    # 在搜索框中输入关键词并提交搜索
    search_box = driver.find_element(By.CLASS_NAME,"imdb-header-search__input")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # 等待搜索结果页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item")))

    # 获取搜索结果中第一个电影的链接
    first_result = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
    print("找到结果:",len(first_result),"个",flush=True)
    if(len(first_result)>0):
        links=first_result[0].find_elements(By.TAG_NAME,'a')
        if(len(links)>0):
            link=links[0]
            movie_url = link.get_attribute("href")
            print("movie Title:",keyword, movie_url,flush=True)
            return {"Title":keyword,"url":movie_url,'time':datetime.datetime.now()}
    return {"Title":keyword,"url":"",'time':datetime.datetime.now()}

def main(index=None,limit=None):
    if(index==None):
        index=1
    driver = get_driver()
    # 打开IMDB网站
    driver.get("https://www.imdb.com/")
    csv_file=f'data/output_{index}.csv'

    datas=[]
    keywords=get_keywords(index,limit)
    count=len(keywords)
    with tqdm(total=count) as pbar:
        for keyword in keywords:
            print("==="*20,flush=True)
            print("keyword:",keyword,flush=True)
            try:
                result=search(driver=driver,keyword=keyword)
                if(result is not None):
                    datas.append(result)
                df = pd.DataFrame(datas, columns=['Title','url','time'])
                try:
                    print("csv 合并中...",flush=True)
                    csv_df=pd.read_csv(csv_file,encoding='utf-8')
                    print("csv 合并中1...",flush=True)
                    # 将数据帧2连接到数据帧1中
                    new_df = pd.concat([csv_df, df], ignore_index=True)
                    print("csv 合并中2...",flush=True)
                    #new_df.drop_duplicates(subset=['url'],keep='last',inplace=True)
                    print("csv 合并中3...",flush=True)
                    new_df.to_csv(csv_file,index=False)
                    print("csv 合并成功",flush=True)
                except Exception as e:
                    print("csv error:",e,flush=True)
                    df.to_csv(csv_file,index=False)
                    print("csv 新建成功",flush=True)
            except Exception as e:
                # 关闭浏览器
                driver.quit()
                driver = get_driver()
                # 打开IMDB网站
                driver.get("https://www.imdb.com/")
                print("error:",e,flush=True)
            pbar.update(1)
    return csv_file