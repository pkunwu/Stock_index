from ntime import ntw
from analysis import analysis
import numpy as np
import matplotlib.pyplot as plt
from distri import distri, std, momentum
from vtwap import pd, vwap
import json


class data(analysis):
    def __init__(self, file='book_20190614.csv', n=500, ts=3000000, mini=100):
        # load data
        test = analysis(file)
        self.data_now = {}
        self.data_pre = {}

        for i in range(n):
            rtw, ss = test.sampling(ts=ts, mini=mini)
            self.data_now[rtw] = stats(test, rtw)
            rtw_pre = (rtw[0]-ts, rtw[1]-ts)
            self.data_pre[rtw_pre] = stats(test, rtw_pre)

# features that will be used in the model.


def stats(cls, tw):
    stats = {}
    vwp = cls.vwap(tw=tw)
    twp = cls.twap(tw=tw)
    stats['vwap'] = vwp
    stats['twap'] = twp

    r, d = cls.arbi(tw=tw)
    stats['arbi_index'] = r

    stats['vwap_momentum'] = momentum(d=vwp)
    vwap_data = []
    for t in vwp.keys():
        vwap_data = vwap_data+[vwp[t]]
    stats['vwap_distri'] = distri(data=vwap_data)
    stats['vwap_std'] = std(ls=vwap_data)

    stats['twap_momentum'] = momentum(d=twp)
    twap_data = []
    for t in twp.keys():
        twap_data = twap_data+[twp[t]]
    stats['twap_distri'] = distri(data=twap_data)
    stats['twap_std'] = std(ls=twap_data)

    a, b = cls.side(tw)
    a_twap_pd = pd(d=a, d1=twp)
    stats['a/twap'] = a_twap_pd
    a_vwap_pd = pd(d=a, d1=vwp)
    stats['a/vwap'] = a_vwap_pd
    b_twap_pd = pd(d=b, d1=twp)
    stats['b/twap'] = b_twap_pd
    b_vwap_pd = pd(d=b, d1=vwp)
    stats['b/vwap'] = b_vwap_pd

    stats['a/twap_distri'] = distri(d=a_twap_pd)
    stats['a/twap_std'] = std(d=a_twap_pd)
    stats['a/vwap_distri'] = distri(d=a_vwap_pd)
    stats['a/vwap_std'] = std(d=a_vwap_pd)
    stats['b/twap_distri'] = distri(d=b_twap_pd)
    stats['b/twap_std'] = std(d=b_twap_pd)
    stats['b/vwap_distri'] = distri(d=b_vwap_pd)
    stats['b/vwap_std'] = std(d=b_vwap_pd)
    return stats
