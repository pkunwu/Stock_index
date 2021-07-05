import sklearn
from results import data
import numpy as np
import json
from sklearn import linear_model
from sklearn import preprocessing
import pandas as pd
# sampling
a = [data(file=f'book_2019061{i}.csv') for i in range(5)]

arbi_index = []
market_index = []
twap_low = []
twap_median = []
twap_high = []
twap_std = []
twap_momentum = []
vwap_low = []
vwap_median = []
vwap_high = []
vwap_std = []
vwap_momentum = []
a_twap_std = []
a_vwap_std = []
b_twap_std = []
b_vwap_std = []

for i in range(5):
    arbi_index = arbi_index + [a[i].data_now[w]
                               ['arbi_index'] for w in a[i].data_now]
    market_index = market_index + \
        [len(a[i].data_now[w]['vwap']) for w in a[i].data_now]
    twap_low = twap_low + \
        [round(a[i].data_now[w]['twap_distri'][1], 2) for w in a[i].data_now]
    twap_median = twap_median + [a[i].data_now[w]
                                 ['twap_distri'][3] for w in a[i].data_now]
    twap_high = twap_high + [a[i].data_now[w]
                             ['twap_distri'][5] for w in a[i].data_now]
    twap_std = twap_std + [a[i].data_now[w]['twap_std'] for w in a[i].data_now]
    twap_momentum = twap_momentum + \
        [a[i].data_now[w]['twap_momentum'] for w in a[i].data_now]
    vwap_low = vwap_low + \
        [round(a[i].data_now[w]['vwap_distri'][1], 2) for w in a[i].data_now]
    vwap_median = vwap_median + [a[i].data_now[w]
                                 ['vwap_distri'][3] for w in a[i].data_now]
    vwap_high = vwap_high + \
        [round(a[i].data_now[w]['vwap_distri'][5], 2) for w in a[i].data_now]
    vwap_std = vwap_std + [a[i].data_now[w]['vwap_std'] for w in a[i].data_now]
    vwap_momentum = vwap_momentum + \
        [a[i].data_now[w]['vwap_momentum'] for w in a[i].data_now]
    a_twap_std = a_twap_std + [np.mean(list(a[i].data_now[w]
                               ['a/twap_std'].values())) for w in a[i].data_now]
    a_vwap_std = a_vwap_std + [np.mean(list(a[i].data_now[w]
                               ['a/vwap_std'].values())) for w in a[i].data_now]
    b_twap_std = b_twap_std + [np.mean(list(a[i].data_now[w]
                               ['b/twap_std'].values())) for w in a[i].data_now]
    b_vwap_std = b_vwap_std + [np.mean(list(a[i].data_now[w]
                               ['b/vwap_std'].values())) for w in a[i].data_now]
# X of Lasso
x = []
for i in range(len(arbi_index)):
    x.append([market_index[i], twap_low[i],
             twap_median[i], twap_high[i], twap_std[i], twap_momentum[i], vwap_low[i], vwap_median[i], vwap_high[i], vwap_std[i], vwap_momentum[i], a_twap_std[i], a_vwap_std[i], b_twap_std[i], b_vwap_std[i]])

train_data = {'y': arbi_index, 'x': x}
with open('train_data.json', 'w') as f:
    json.dump(train_data, f)

with open('train_data.json', 'r') as f:
    train_data = json.load(f)

x = train_data['x']
y = train_data['y']

clf = linear_model.Lasso()
clf.fit(x, y)
coef = clf.coef_
inter = clf.intercept_

clf_nor = linear_model.Lasso(normalize=True)
clf_nor.fit(x, y)
coef_nor = clf_nor.coef_
inter_nor = clf_nor.intercept_
