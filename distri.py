# data is a list or 1d np.array
import numpy as np


def distri(*, data=None, d=None):
    if data is None and d is None:
        return None
    if data is not None:
        nandata = np.array([x for x in data if x])
        ratio = round(len(nandata)/len(data), 2)
        mean = np.mean(data)
        min = np.nanmin(data)
        q1 = np.nanquantile(data, 0.25)
        q2 = np.nanquantile(data, 0.50)
        q3 = np.nanquantile(data, 0.75)
        max = np.nanmax(data)
        return ratio, mean, min, q1, q2, q3, max
    if d is not None:
        rs = {}
        for t in d.keys():
            ls = [x for x in d[t] if x]
            if ls != []:
                rs[t] = (round(np.mean(d[t]), 2), round(np.nanmin(d[t]), 2), round(np.nanquantile(d[t], 0.25), 2), round(
                    np.nanquantile(d[t], 0.50), 2), round(np.nanquantile(d[t], 0.75), 2), round(np.nanmax(d[t]), 2))
        return rs


def std(*, ls=None, d=None):
    if ls is None and d is None:
        return None
    if ls is not None:
        if len(ls) <= 1:
            Warning('list is too short.')
        ls = np.array([x for x in ls if x is not None])
        return round(np.nanstd(ls), 2)
    if d is not None:
        rs = {}
        for t in d.keys():
            rs[t] = round(np.nanstd(d[t]), 2)
        return rs


def momentum(*, ls=None, d=None):
    if ls is None and d is None:
        return None
    if ls is not None:
        if len(ls) <= 1:
            raise KeyError('list is too short.')
        ls = np.array([x for x in ls if x is not None])
        return round(np.log(ls[-1]/ls[0]), 5)
    if d is not None:
        keys = list(d.keys())
        st = np.min(keys)
        et = np.max(keys)
        return round(np.log(np.mean(d[et])/np.mean(d[st])), 5)
