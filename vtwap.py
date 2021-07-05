# ls of orders, dict: time -> id. t, tw.
import warnings
from ntime import nt, ntw
import numpy as np
# ls must be sorted d.keys().


def vwap(*, d, ls, t=None, tw=None):
    if t and tw:
        Warning('only time will be used. time window will be ignored.')
    if t is not None:
        v = 0
        time = nt(t, ls)
        for line in d[time]:
            bv, bq, av, aq = line[1:5]
            v += round((bv+av)/(bq+aq), 2)
        return round(v/len(d[time]), 2)
    if tw is not None:
        rs = {}
        for t in ntw(tw, ls):
            rs[t] = vwap(d=d, ls=ls, t=t)
        return rs
    else:
        return vwap(tw=(0, 36000000000), ls=ls, d=d)


def twap(*, orders, d, ls, t=None, tw=None):
    if t and tw:
        raise Warning('only time will be used. time window will be ignored.')
    if not(t is None):
        time = nt(t, ls)
        return round(sum([orders[x[0]].t[time][1] for x in d[time]])/len(d[time]), 2)
    if tw is not None:
        rs = {}
        for t in ntw(tw, ls):
            rs[t] = twap(orders=orders, d=d, ls=ls, t=t)
        return rs
    if t is None and tw is None:
        Warning('running time will be long.')
        return twap(orders=orders, d=d, ls=ls, tw=(0, 36000000000))

# difference of prices between a given dict and vwap


def pd(*, d, d1):
    if isinstance(d, dict) and isinstance(d1, dict):
        d_d1_pd = {}
        for i in d.keys():
            for j in d[i]:
                if i in d_d1_pd.keys():
                    d_d1_pd[i].append(round(j.t[i][1]-d1[i], 2))
                else:
                    d_d1_pd[i] = [round(j.t[i][1]-d1[i], 2)]
        return d_d1_pd
    elif isinstance(d, d1):
        return round(d-d1, 2)
    else:
        raise KeyError('types are not supported.')


# test
# file = 'book_20190610.csv'
# test = analysis(file)
# d = test.to
# orders = test.orders
# t = 0
# tw = (1000000,2000000)
# vwap(d = d, ls = ls,  t = t)
# g = vwap(d=d, ls = ls, tw = tw)
# twap(orders = orders, d = d, t = t)
# twap(orders= orders, d= d, tw= tw)
#twap(d = d, orders = orders)
# t = 20341195530
# ls = np.array(sorted(test.to.keys()))
