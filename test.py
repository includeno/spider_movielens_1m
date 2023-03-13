from tqdm import tqdm
import time
from spider import main
import numpy as np
import pandas as pd

with tqdm(total=100) as pbar:
    for i in range(100):
        #time.sleep(0.1)
        pbar.update(1)

# 将数据帧分割为n个子数据帧
# n = 6
# df=pd.read_csv('data/input.csv',encoding='utf-8')
# dfs = np.array_split(df, n)
# for i in range(len(dfs)):
#     dfs[i].to_csv('data/input_'+str(i)+'.csv',index=False,encoding='utf-8')

file_path=main(1,3)