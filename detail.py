import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import concurrent.futures

# url = 'https://www.imdb.com/title/tt0468569/'

import pymysql

def create_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root123456',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_aws_connection():
    connection = pymysql.connect(host='dbs-mysql.cirpywua5kjp.ap-east-1.rds.amazonaws.com',
                            user='admin',
                            password='nacos4HBlv3==',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_urls(count):
    connection=create_connection()
    cursor=connection.cursor()
    if(count==None):
        count=10
    # 查询语句
    sql = f"SELECT id, name,full_name, url FROM imdb_movies_links_full WHERE spider_completed=0 and url not in (select url from imdb_movies) LIMIT {count}"

    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def remove_pair(text):
    # 要处理的文本内容
    #text = "xyzydasd($534,987,076)"

    # 匹配括号及括号内的内容
    pattern = re.compile(r'\([^)]*\)')

    # 替换匹配到的内容为空字符串
    text2 = pattern.sub('', text)
    return text2

def get_driver():
    # 设置Firfox浏览器选项
    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    # 创建Firfox浏览器实例
    driver = webdriver.Firefox(options=options)
    # 最小化窗口
    #driver.minimize_window()
    return driver

def get_movie_detail(movie_item,mysql_save=False):
    url=movie_item['url']
    # 启动Chrome浏览器
    driver = get_driver()
    # 打开网页
    driver.get(url)

    # 获取页面源代码
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    #print(html)
    soup = BeautifulSoup(html, 'html.parser')

    # 电影标题
    title = soup.find('h1').text.strip()

    # 电影时长
    time=None
    for time_li in soup.select('li.ipc-metadata-list__item:-soup-contains("Runtime")'):
        for item in time_li.select('div.ipc-metadata-list-item__content-container'):
            time=item.text.strip()
        break

    # 电影发布时间
    release_date=None
    for release_date_li in soup.select('li.ipc-metadata-list__item:-soup-contains("Release date")'):
        for item in release_date_li.select('a.ipc-metadata-list-item__list-content-item--link'):
            release_date=item.text.strip()
            release_date=remove_pair(release_date)
        break

    # 电影简介
    intro=""
    intro = soup.select_one('span[data-testid="plot-xl"]').text.strip()

    # 电影类型
    genres=[]
    for genre_div in soup.select('div.ipc-chip-list__scroller'):
        for item in genre_div.select('a.ipc-chip--on-baseAlt'):
            genres.append(item.text.strip())
        break

    # 导演信息
    directors = []
    for director in soup.select('li.ipc-metadata-list__item:-soup-contains("Director")'):
        for item in director.select('a.ipc-metadata-list-item__list-content-item--link'):
            directors.append(remove_pair(item.text.strip()))
        break

    # 演员信息
    writers = []
    for writer in soup.select('li.ipc-metadata-list__item:-soup-contains("Writers")'):
        for item in writer.select('a.ipc-metadata-list-item__list-content-item--link'):
            writers.append(remove_pair(item.text.strip()))
    for writer in soup.select('li.ipc-metadata-list__item:-soup-contains("Writer")'):
        for item in writer.select('a.ipc-metadata-list-item__list-content-item--link'):
            writers.append(remove_pair(item.text.strip()))

    # 演员信息
    actors = []
    for actor in soup.select('li.ipc-metadata-list__item:-soup-contains("Stars")'):
        for item in actor.select('a.ipc-metadata-list-item__list-content-item--link'):
            actors.append(remove_pair(item.text.strip()))
    for actor in soup.select('li.ipc-metadata-list__item:-soup-contains("Star")'):
        for item in actor.select('a.ipc-metadata-list-item__list-content-item--link'):
            actors.append(remove_pair(item.text.strip()))

    print("===="*20)
    print(url)
    print("电影标题:", title)
    print("电影简介:", intro)
    print("导演:", list(set(directors)))
    print("演员:", list(set(actors)))
    print("电影类型:", list(set(genres)))
    print("发布时间:",release_date)
    print('电影时长:',time)

    if(mysql_save==True):
        pass
    return {"name":title,"full_name":movie_item['full_name'],"url":url,"time":time,"genre":'|'.join(list(set(genres))),"release_time":release_date,"intro":intro,"directors":'|'.join(list(set(directors))),"writers":'|'.join(list(set(writers))),"actors":'|'.join(list(set(actors)))}

movie_list=get_urls(1100)
# for url in urls:
#     get_movie_detail(url,mysql_save=False)

# 创建一个线程列表
threads = []

# 创建一个线程池，指定最大线程数为 3
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # 定义一组任务列表
    args = [1, 2, 3, 4, 5]

    # 提交任务到线程池，并获取对应的 Future 对象
    futures = [executor.submit(get_movie_detail,item,True) for item in movie_list]

    # 遍历 Future 对象，获取执行结果
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print(f"The result is {result}")
            connection=create_connection()
            cursor=connection.cursor()
            try:
                cursor.execute(""" INSERT INTO imdb_movies (name,full_name, url, time, genre, release_time, intro, directors, writers,starts, completed)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s); """, (
                        result['name'],result['full_name'],
                        result['url'],
                        result['time'],result['genre'],result['release_time'],result['intro'],result['directors'],result['writers'],result['actors'],'1'
                    ))
                #更新links表
                sql = "UPDATE imdb_movies_links_full SET spider_completed=1 WHERE url=%s"
                print("update links",sql)
                # 执行更新
                data = [result['url']]
                cursor.executemany(sql, data)
                connection.commit()
            except:
                print("MYSQL error")