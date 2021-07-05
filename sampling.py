#generate random sampling. with a minimum given data size.
from ntime import ntw, ntw_order_count
import numpy as np
def sampling_tw(to, ls, ts, mini=1000):
    while True:
        st = round(np.random.uniform()*36000000000)
        et = st+ts
        num = ntw_order_count((st,et), ls, to)
        if num > mini and et<36000000000 and st-ts>=0 and ntw_order_count(((st-ts), (et-ts)),ls,to)>mini:
            print(f'time window: ({st},{et}). order number: {num}.')
            break
    return (st,et), num


# test
# to = {}
# for i in range(360):
#     to[i] = range(i)
# ts = 1000000
# sampling_tw(to)
