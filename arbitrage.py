import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
#load data.
columns_volumn = ['timestamp','av','bv','aq','bq']
files = ['book_20190610.csv','book_20190611.csv','book_20190612.csv','book_20190613.csv','book_20190614.csv']
columns_price = ['id','timestamp', 'price', 'side' ,'action']
# columns_tops = ['timestamp', 'bp0','bq0','bp1','bq1','bp2','bq2','ap0','aq0','ap1','aq1','ap2','aq2']
volumn_datas =  [pd.read_csv(file, usecols = columns_volumn) for file in files]
price_datas = [pd.read_csv(file, usecols = columns_price) for file in files]

b_price_datas = [price_data[price_data.side == 'b'] for price_data in price_datas]
a_price_datas = [price_data[price_data.side == 'a'] for price_data in price_datas]

b_price_datas_no_d = [x[x.action != 'd'] for x in b_price_datas]
a_price_datas_no_d = [x[x.action != 'd'] for x in a_price_datas]

# arbitrages chances in 1s. i.e., b_price > a_price within 1,000,000.
# take a pair of dfs as input. return a dictionary of indexes of dfs.
def arbitrages(buy = None, sell = None):
    arbitrage = {}
    for i in buy.index:
        for j in sell[(sell['timestamp']-buy['timestamp'][i]<1000000) & (sell['timestamp']>buy['timestamp'][i])].index:
            if buy['price'][i] > sell['price'][j]:
                try:
                    arbitrage[i].append(j)
                except:
                    arbitrage[i] = [j]
    for j in sell.index:
        for i in buy[(buy['timestamp']-sell['timestamp'][j]<1000000) & (buy['timestamp']>sell['timestamp'][j])].index:
            if buy['price'][i] > sell['price'][j]:
                try:
                    arbitrage[j].append(i)
                except:
                    arbitrage[j] = [i]
    return arbitrage

#locate 1s time window for each arbitrage. take d,df return a dict of time windows starting point.
def tw_arbi(arbi_d, df):
    tw_ls = {}
    keys = [int(i) for i in arbi_d.keys()]
    keys.sort()
    for i in keys:
        start_ts = max(0, df['timestamp'][i]-1000000)
        start_t = max(0,df['timestamp'][df['timestamp'] <= start_ts].max())
        start_i = df[df['timestamp'] == start_t].index.min() # 1s in advance.
        end_ts = min(df['timestamp'].iloc[-1] , df['timestamp'][i]+1000000)
        end_t = min(df['timestamp'].iloc[-1], df['timestamp'][df['timestamp'] <= end_ts].max())
        end_i = df[df['timestamp'] == end_t].index.max()+1
        tw_ls[i] = (start_i,end_i)
    return tw_ls

# arbitrage_datas = [arbitrages(buy= b_price_datas_no_d[i], sell=a_price_datas_no_d[i]) for i in range(5)]
arbi_ds = []
for i in range(5):
    with open(f'arbitrage_2019061{i}.json', 'r') as f:
        arbi_ds.append(json.load(f))

# for i in range(5):
#     with open(f'arbitrage_2019061{i}.json', 'w') as f:
#         json.dump(arbi_ds[i],f, sort_keys=True)

tw_dfs = [tw_arbi(arbi_ds[i],price_datas[i]) for i in range(5)]

class tw_stats(object):
    def __init__(self, arbi_d, tw_d, df):
        self.arbi_d = arbi_d
        self.tw_d = tw_d
        self.df = df
    
    #mean price per timestamp
    def mean_price(self):
        m_p = self.df['price'].groupby('timestamp').agg(mean = ('price', 'mean'),)
        return m_p
    
    #momentum of first 1s.
    def momentum(self):
        m_p = self.mean_price()
        start_p = m_p['mean']
        end_p = m_p['mean'][]