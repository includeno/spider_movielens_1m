import pandas as pd

num=11
nan=pd.read_csv('data/nan.csv',encoding='utf-8')
nan.drop({'id','genres','release_time','directors','writers','starts'},axis=1,inplace=True)
nan = nan.assign(url=pd.Series())
nan = nan.assign(create_time=pd.Series())
nan.to_csv(f'data/inupt_{num}.csv',encoding='utf-8',index=False)