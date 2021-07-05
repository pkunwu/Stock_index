# takes tw, to, ls,  return two lists of orders of given side.
from ntime import ntw


def side(tw, to, ls, orders):
    a = {}
    b = {}
    if tw is None:
        return side((0, 36000000000), to, ls, orders)
    for i in ntw(tw=tw, ls=ls):
        for j in to[i]:
            if orders[j[0]].t[i][0] != 'm':
                if orders[j[0]].s == 'a':
                    try:
                        a[i].append(orders[j[0]])
                    except:
                        a[i] = [orders[j[0]]]
                else:
                    try:
                        b[i].append(orders[j[0]])
                    except:
                        b[i] = [orders[j[0]]]
    return a, b
