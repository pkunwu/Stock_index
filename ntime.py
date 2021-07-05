#ls must be sorted. 
#find the nearest time.
import numpy as np
def nt(time, ls, method = None):
    if method is None:
        return ls[ls<=time].max()
    if method == 'rv':
        return ls[ls>=time].min()

#takes tw, ls, return a list of time in tw.
def ntw(tw,ls):
    if len(tw)!= 2:
        raise KeyError('missing time window.')
    
    if tw[0]>tw[1]:
        return []

    return [i for i in ls[(tw[0]<=ls)&(ls<=tw[-1])]]
        

#takes a tw and a dict to, return the count of order in tw.
def ntw_order_count(tw, ls, to):
    return sum([len(to[x]) for x in ntw(tw, ls)])

#test
# time = 3
# tw = (1,7)
# to = {}
# for i in range(7):
#     to[2*i] = range(i)
# nt(time = time, ls = to.keys())
# ntw(tw = tw, ls = to.keys())
# ntw_order_count(tw, ls, to)
