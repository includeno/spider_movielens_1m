import pandas as pd
from selenium_driver import get_driver
import datetime
from tqdm import tqdm
import time
import re
from bs4 import BeautifulSoup

def main(index,limit=None):
    if(index==None):
        index=0
    # 获取电影信息
    df_movies = get_inputs(index,limit)
    count=len(df_movies)
    with tqdm(total=count) as pbar:
        #遍历所有行
        for df_index, row in df_movies.iterrows():
            print("===="*20,f"正在爬取第{df_index+1}条数据",flush=True)
            # 获取电影详情页链接
            movie_url = row['url']
            # 获取电影信息
            movie_info = get_movie_info(movie_url)
            if(movie_info is not None):
                # 将电影信息添加到数据帧中
                df_movies.loc[df_index, 'spider_time'] = datetime.datetime.now()
                df_movies.loc[df_index, 'title'] = movie_info['title']
                df_movies.loc[df_index, 'time'] = movie_info['time']
                df_movies.loc[df_index, 'release_date'] = movie_info['release_date']
                df_movies.loc[df_index, 'intro'] = movie_info['intro']
                df_movies.loc[df_index, 'genres'] = movie_info['genres']
                df_movies.loc[df_index, 'directors'] = movie_info['directors']
                df_movies.loc[df_index, 'writers'] = movie_info['writers']
                df_movies.loc[df_index, 'actors'] = movie_info['actors']
            pbar.update(1)
            time.sleep(1)
            print("\n\n")
            print("movie_info:",movie_info,flush=True)
            # 保存数据
            df_movies.to_csv(f'data/output_{index}.csv', index=False, encoding='utf-8')
        


def get_inputs(index,limit=None):
    movies=pd.read_csv(f'data/input_{index}.csv',encoding='utf-8')
    # 使用 assign() 方法添加一个空列
    movies = movies.assign(spider_time=pd.Series())
    movies = movies.assign(title=pd.Series())
    movies = movies.assign(time=pd.Series())
    movies = movies.assign(release_date=pd.Series())
    movies = movies.assign(intro=pd.Series())
    movies = movies.assign(genres=pd.Series())
    movies = movies.assign(directors=pd.Series())
    movies = movies.assign(writers=pd.Series())
    movies = movies.assign(stars=pd.Series())

    movies.fillna('', inplace=True)
    print(movies.head())
    if(limit==None):
        return movies
    return movies.head(limit)

def remove_pair(text):
    # 要处理的文本内容
    #text = "xyzydasd($534,987,076)"

    # 匹配括号及括号内的内容
    pattern = re.compile(r'\([^)]*\)')

    # 替换匹配到的内容为空字符串
    text2 = pattern.sub('', text)
    return text2

def get_movie_info(movie_url):
    
    # 启动浏览器
    driver = get_driver(page_load_timeout=8)
    html=None
    try:
        # 打开电影详情页
        driver.get(movie_url)
        # 获取页面源代码
        html = driver.page_source
    except:
        # 获取页面源代码
        html = driver.page_source
    finally:
        # 关闭浏览器
        driver.quit()
    
    if(html==None):
        return None
    
    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(html, 'html.parser')

    # 获取电影标题
    title = soup.find('h1').text.strip()

    # 获取电影时长
    time = None
    for time_li in soup.select('li.ipc-metadata-list__item:-soup-contains("Runtime")'):
        for item in time_li.select('div.ipc-metadata-list-item__content-container'):
            time = item.text.strip()
        break

    # 获取电影发布时间
    release_date = None
    for release_date_li in soup.select('li.ipc-metadata-list__item:-soup-contains("Release date")'):
        for item in release_date_li.select('a.ipc-metadata-list-item__list-content-item--link'):
            release_date = item.text.strip()
            release_date = remove_pair(release_date)
        break

    # 获取电影简介
    intro = soup.select_one('span[data-testid="plot-xl"]').text.strip()

    # 获取电影类型
    genres = []
    for genre_div in soup.select('div.ipc-chip-list__scroller'):
        for item in genre_div.select('a.ipc-chip--on-baseAlt'):
            genres.append(item.text.strip())
        break
    genres_str='|'.join(genres)

    # 获取导演信息
    directors = []
    for director in soup.select('li.ipc-metadata-list__item:-soup-contains("Director")'):
        for item in director.select('a.ipc-metadata-list-item__list-content-item--link'):
            directors.append(remove_pair(item.text.strip()))
        break
    directors_str='|'.join(directors)

    # 获取编剧信息
    writers = []
    for writer in soup.select('li.ipc-metadata-list__item:-soup-contains("Writers")'):
        for item in writer.select('a.ipc-metadata-list-item__list-content-item--link'):
            writers.append(remove_pair(item.text.strip()))
    for writer in soup.select('li.ipc-metadata-list__item:-soup-contains("Writer")'):
        for item in writer.select('a.ipc-metadata-list-item__list-content-item--link'):
            writers.append(remove_pair(item.text.strip()))
    writers_str='|'.join(writers)

    # 获取演员信息
    actors = []
    for actor in soup.select('li.ipc-metadata-list__item:-soup-contains("Stars")'):
        for item in actor.select('a.ipc-metadata-list-item__list-content-item--link'):
            actors.append(remove_pair(item.text.strip()))
    for actor in soup.select('li.ipc-metadata-list__item:-soup-contains("Star")'):
        for item in actor.select('a.ipc-metadata-list-item__list-content-item--link'):
            actors.append(remove_pair(item.text.strip()))
    actors_str='|'.join(actors)

    # 构建电影信息的字典对象
    movie_info = {"title": title, "url": movie_url, "time": time, "genres": genres_str, "release_date": release_date,
                "intro": intro, "directors": directors_str, "writers": writers_str, "actors": actors_str}

    return movie_info
