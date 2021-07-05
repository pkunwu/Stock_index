# order object. use update function to add more actions.
from os import error

class order(object):
    def __init__(self, **kw) -> None:
        if 'id' not in kw.keys():
            raise KeyError('missing id.')
        else:
            self.id = int(kw['id'])
        if 's' not in kw.keys():
            raise KeyError('missing side.')
        else:
            self.s = kw['s']
        if 't' not in kw.keys():
            raise KeyError('missing timestamp.')
        if 'a' not in kw.keys():
            raise KeyError('missing action.')
        if 'p' not in kw.keys():
            raise KeyError('missing price.')
        if 'q' not in kw.keys():
            raise KeyError('missing quantity')
        self.t = {int(kw['t']) : (kw['a'],int(kw['p']),int(kw['q']))}

    def update(self, **kw):
        if 't' not in kw.keys():
            raise KeyError('missing timestamp.')
        if 'a' not in kw.keys():
            raise KeyError('missing action.')
        if 'p' not in kw.keys():
            raise KeyError('missing price.')
        if 'q' not in kw.keys():
            raise KeyError('missing quantity')
        self.t[int(kw['t'])] = (kw['a'],int(kw['p']),int(kw['q']))

    def ts(self):
        key = sorted(self.t.keys())
        if 'd' not in self.t[key[-1]]:
            return None
        else:
            return key[-1]-key[0]

    def pd(self):
        pd = 0
        for i in sorted(self.t.keys()):
            try:
                pd += abs(self.t[i][1]-self.t[i-1][1])
            except:
                pass
        return pd

# test
# orders = {}
# with open('res_20190610.csv','r') as f:
#     line = f.readlines()
#     for i in range(1,len(line)):
#         t,s,a,id,p,q = line[i].split('\n')[0].split(',')
#         if int(id) not in orders.keys():
#             orders[int(id)] = order(id = int(id), s = s, t = int(t), a = a, p = int(p), q = int(q))
#         else:
#             orders[int(id)].update(t = int(t), a = a, p = int(p), q = int(q))