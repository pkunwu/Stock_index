from numpy.core.fromnumeric import size, sort
from numpy.lib.function_base import percentile
import re
from order import order
import numpy as np
import matplotlib.pyplot as plt
from ntime import nt, ntw
import vtwap
from arbitrage import arbitrages
from sampling import sampling_tw
from side import side
# time span of a order.
class analysis(object):
    def __init__(self, file):
        self.orders = {}
        self.to = {}
        with open(file,'r') as f:
            line = f.readlines()
            for i in range(1,len(line)):
                num = [int(x) for x in re.findall(r'(\d+)',line[i])]
                char = re.findall(r'([a-z]),',line[i])
                if num[1] in self.orders.keys():
                    self.orders[num[1]].update(t = num[0], a = char[1], p = num[2], q = num[3])
                else:
                    self.orders[num[1]] = order(id = num[1], s = char[0], t = num[0], a = char[1], p = num[2], q = num[3])
                if num[0] in self.to.keys():
                    self.to[num[0]].append((num[1], num[-4], num[-3], num[-2], num[-1], num[6:]))
                else:
                    self.to[num[0]] = [(num[1], num[-4], num[-3], num[-2], num[-1], num[6:])]
        self.ts = np.array(sorted(self.to.keys()))

    def vwap(self, time = None, tw = None):
        return vtwap.vwap(d = self.to, ls= self.ts, t=time, tw =tw)

    def twap(self, time = None, tw = None):
        return vtwap.twap(orders=self.orders, d=self.to, ls= self.ts, t=time, tw=tw)
    
    def arbi(self, tw = None):
        return arbitrages(tw=tw, orders=self.orders, to = self.to, ls= self.ts)

    # def momentum(self, gen):
    #     ls = [x for x in gen if x]
    #     if len(ls)<=1:
    #         raise KeyError('list is too short.')
    #     return round(np.log(ls[-1]/ls[0]),5)

    # def std(self, gen):
    #     ls = [x for x in gen if x]
    #     if len(ls)<=1:
    #         raise KeyError('list is too short.')
    #     return np.nanstd(ls)

    # def distri(self, ls,**kw):
    #     nandata = np.array([x for x in ls if x])
    #     ratio = round(len(nandata)/len(ls) ,2)
    #     mean = np.mean(ls)
    #     min = np.nanmin(ls)
    #     q1 = np.nanquantile(ls, 25)
    #     q2 = np.nanquantile(ls, 50)
    #     q3 = np.nanquantile(ls, 75)
    #     max = np.nanmax(ls)
    #     return ratio, mean, min, q1, q2, q3, max

    def sampling(self, ts = 1000000, mini = 100):
        return sampling_tw(self.to, self.ts, ts = ts, mini = mini)

    def side(self, tw = None):
        return side(tw, to = self.to, ls= self.ts, orders = self.orders)
                
#test
# file = 'book_20190614.csv'
# test = analysis(file)
# rtw, ss = test.sampling(ts = 1000000, mini = 100)
# a = test.vwap(tw = rtw)
# b = test.twap(tw = rtw)
# r, d = test.arbi(tw = rtw)
# s = set(d.keys())
# rs = [test.orders[dt].ts() for dt in s]
# np.nanquantile(rs, 0.5)
# np.nanmean(rs)
# test.momentum(b)
# test.std(a)
