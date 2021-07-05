# arbitrages chances in 1s. i.e., b_price > a_price within 1,000,000.
# take a pair time, dict: id->order, dict: timestamp->id. return a dictionary of indexes of dfs: arbi_i_start -> arbi_i_end.
from order import order
import warnings
from ntime import nt, ntw
import numpy as np

def arbitrages(tw = None, *, orders, to, ls):
    if orders is None or to is None:
        raise KeyError('missing timestamp.')
    if tw is None:
        Warning('running time will be long.')
        return arbitrages(tw = (0,36000000000), orders = orders, to = to, ls=ls)
    arbitrage = {}
    for i in ntw(tw, ls):
        for j in ntw((i+1,tw[1]), ls):
            for k in to[i]:
                for l in to[j]:
                    id_i = k[0]
                    id_j = l[0]
                    p_i = orders[id_i].t[i][1]; a_i = orders[id_i].t[i][0]; s_i = orders[id_i].s
                    p_j = orders[id_j].t[j][1]; a_j = orders[id_j].t[j][0]; s_j = orders[id_j].s
                    if s_i != s_j and a_i != 'm' and a_j != 'm':
                        if (s_i == 'b' and p_i > p_j) or (s_i == 'a' and p_i < p_j):
                            try:
                                arbitrage[id_i].append(id_j)
                            except:
                                arbitrage[id_i] = [id_j]
    arbi_set = set(arbitrage.keys())
    
    b_s = [len(arbitrage[x]) for x in arbi_set if orders[x].s == 'b']
    a_s = [len(arbitrage[x]) for x in arbi_set if orders[x].s == 'a']
    try:
        rate = round((sum(b_s)+ sum(a_s))/len(ntw(tw, ls)),2)
    except ZeroDivisionError:
        rate = 0
    return rate, arbitrage


# test
# tw = (0,1000000)
# orders = test.orders
# to = test.to
# ls = test.ts
# rate, d = arbitrages(tw = tw, orders = orders, to = to, ls = test.ts)
