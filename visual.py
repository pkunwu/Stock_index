import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
columns = ['timestamp','av','bv','aq','bq']
files = ['book_20190610.csv','book_20190611.csv','book_20190612.csv','book_20190613.csv','book_20190614.csv']
volumn_datas =  [pd.read_csv(file, usecols = columns) for file in files]

for volumn_data in volumn_datas:
    volumn_data['VWAP'] = round((volumn_data.bv+volumn_data.av)/(volumn_data.bq+volumn_data.aq),2)
    volumn_data['bv_over_av'] = volumn_data.bv - volumn_data.av

vwaps = [volumn_data.groupby('timestamp').agg(VWAP = ("VWAP", "last"),) for volumn_data in volumn_datas]
bvs = [volumn_data.groupby('timestamp').agg(bv = ("bv", "last"),) for volumn_data in volumn_datas]
avs = [volumn_data.groupby('timestamp').agg(av = ("av", "last"),) for volumn_data in volumn_datas]
bv_over_avs = [volumn_data.groupby('timestamp').agg(bv_over_av = ('bv_over_av','last'),) for volumn_data in volumn_datas]

# VWAP_min = VWAP.groupby(lambda x: x//3600).agg('min')
# bv_min = bv.groupby(lambda x: x//3600).agg('min')
# VWAP_max = VWAP.groupby(lambda x: x//3600).agg('max')
# bv_max = bv.groupby(lambda x: x//3600).agg('max')
# VWAP_f = VWAP.groupby(lambda x: x//3600).agg('first')
# bv_f = bv.groupby(lambda x: x//3600).agg('first')
# VWAP_l = VWAP.groupby(lambda x: x//3600).agg('last')
# bv_l = bv.groupby(lambda x: x//3600).agg('last')

for vwap in vwaps:
    vwap.plot()
figs, ax = plt.subplots(2,1)
ax[0].plot(vwaps[0].index, vwaps[0].VWAP)
ax[0].set_ylabel('0610 VAMP')
ax[0].grid(True)
ax[1].plot(bv_over_avs[0].index, bv_over_avs[0].bv_over_av)
ax[1].set_ylabel('0610 bv over av')
# ax[1].set_xlimit(0,36000000000)
# ax[1].set_ylimit(bv_over_avs[0].min(),bv_over_avs[0].max())
ax[1].grid(True)
plt.show()