# the class of rows from data. t for timestamp, s for side, a for action, id for id, p for price, q for quantity.
class row_data(object):
    def __init__(self, t, s, a, id, p, q):
        self.t = t
        self.s = s
        self.a = a
        self.id = id
        self.p = p
        self.q = q


class book(row_data):
    # dictionary: price -> set of id.
    ap = {}
    bp = {}
    # dictionary: id -> (p,q)
    ad = {}
    bd = {}
    # top price level
    top = [0, 0, 0, 0, 0]
    # bottom price level
    bottom = [0, 0, 0, 0, 0]
    # buy side volumn
    bv = 0
    # sell side volumn
    av = 0
    # buy side total quantity
    bq = 0
    # sell side total quantity
    aq = 0

    def __init__(self, row_data=None):
        self.row_data = row_data
        if row_data.s == 'a':
            if row_data.a == 'a':
                self.alevel_update_a()
                self.av_update_a()
                self.aq_update_a()
                self.apad_update_a()

            elif row_data.a == 'd':
                self.alevel_update_d()
                self.av_update_d()
                self.aq_update_d()
                self.apad_update_d()

            elif row_data.a == 'm':
                self.alevel_update_m()
                self.av_update_m()
                self.aq_update_m()
                self.apad_update_m()

        else:
            if row_data.a == 'a':
                self.blevel_update_a()
                self.bv_update_a()
                self.bq_update_a()
                self.bpbd_update_a()

            elif row_data.a == 'd':
                self.blevel_update_d()
                self.bv_update_d()
                self.bq_update_d()
                self.bpbd_update_d()

            elif row_data.a == 'm':
                self.blevel_update_m()
                self.bv_update_m()
                self.bq_update_m()
                self.bpbd_update_m()

    # action is add
    def apad_update_a(self):
        # add or update price value to ap and ad.
        if self.row_data.p not in self.ap.keys():
            self.ap[self.row_data.p] = set([self.row_data.id])
        else:
            self.ap[self.row_data.p].add(self.row_data.id)
        self.ad[self.row_data.id] = (self.row_data.p, self.row_data.q)

    def bpbd_update_a(self):
        # add or update price value to bp and bd.
        if self.row_data.p not in self.bp.keys():
            self.bp[self.row_data.p] = set([self.row_data.id])
        else:
            self.bp[self.row_data.p].add(self.row_data.id)
        self.bd[self.row_data.id] = (self.row_data.p, self.row_data.q)

    # action is delete.
    def apad_update_d(self):
        # the removal id is not the only id
        if len(self.ap[self.ad[self.row_data.id][0]]) > 1:
            self.ap[self.ad[self.row_data.id][0]].remove(self.row_data.id)
        else:
            # the removal id is the only id
            self.ap.pop(self.ad[self.row_data.id][0])
        self.ad.pop(self.row_data.id)  # remove the id

    def bpbd_update_d(self):
        if len(self.bp[self.bd[self.row_data.id][0]]) > 1:
            self.bp[self.bd[self.row_data.id][0]].remove(self.row_data.id)
        else:
            self.bp.pop(self.bd[self.row_data.id][0])
        self.bd.pop(self.row_data.id)

    # action is modify.
    def apad_update_m(self):
        self.apad_update_d()
        self.apad_update_a()

    def bpbd_update_m(self):
        self.bpbd_update_d()
        self.bpbd_update_a()

    # update the levels. when action is add.
    def blevel_update_a(self):
        if self.row_data.p > self.top[4]:  # check if top need to be changed
            if self.row_data.p not in self.top:  # check if top already has the value
                for i in range(5):
                    if self.top[i] < self.row_data.p:
                        self.top.insert(i, self.row_data.p)
                        self.top.pop(5)
                        break

    def alevel_update_a(self):
        if self.row_data.p < self.bottom[4] or (self.bottom[4] == 0):
            if self.row_data.p not in self.bottom:
                for i in range(5):
                    if self.bottom[i] > self.row_data.p or self.bottom[i] == 0:
                        self.bottom.insert(i, self.row_data.p)
                        self.bottom.pop(5)
                        break

    # update the levels when action is d.
    def blevel_update_d(self):
        # remove the price from the list if only one id
        if self.bd[self.row_data.id][0] in self.top and len(self.bp[self.bd[self.row_data.id][0]]) == 1:
            self.top.remove(self.bd[self.row_data.id][0])
            try:
                self.top.append(sorted(self.bp.keys(), reverse=True)[
                                5])  # add a new price to list
            except:
                self.top.append(0)

    def alevel_update_d(self):
        # remove the price from the list
        if self.ad[self.row_data.id][0] in self.bottom and len(self.ap[self.ad[self.row_data.id][0]]) == 1:
            self.bottom.remove(self.ad[self.row_data.id][0])
            try:
                self.bottom.append(sorted(self.ap.keys(), reverse=False)[
                                   5])  # add a new price to list
            except:
                self.bottom.append(0)

    # update the levels when action is m.
    def alevel_update_m(self):
        self.alevel_update_d()
        self.alevel_update_a()

    def blevel_update_m(self):
        self.blevel_update_d()
        self.blevel_update_a()

    # update the volumn when action is a.
    def av_update_a(self):
        book.av += self.row_data.p * self.row_data.q

    def bv_update_a(self):
        book.bv += self.row_data.p * self.row_data.q

    # update the volumn when action is d.
    def av_update_d(self):
        book.av -= self.ad[self.row_data.id][0] * self.ad[self.row_data.id][1]

    def bv_update_d(self):
        book.bv -= self.bd[self.row_data.id][0] * self.bd[self.row_data.id][1]

    # update the volumn when action is m.
    def av_update_m(self):
        book.av_update_d(self)
        book.av_update_a(self)

    def bv_update_m(self):
        book.bv_update_d(self)
        book.bv_update_a(self)

    # update the total q when action is a.
    def aq_update_a(self):
        book.aq += self.row_data.q

    def bq_update_a(self):
        book.bq += self.row_data.q

    # update the total q when action is d.
    def aq_update_d(self):
        book.aq -= self.ad[self.row_data.id][1]

    def bq_update_d(self):
        book.bq -= self.bd[self.row_data.id][1]

    # update the total q when action is m.
    def aq_update_m(self):
        book.aq_update_d(self)
        book.aq_update_a(self)

    def bq_update_m(self):
        book.bq_update_d(self)
        book.bq_update_a(self)

    # quantity of a price level.
    def p_to_q(self, s, p):
        q = 0
        if p == 0:
            return q
        if s == 'a':
            for id in self.ap[p]:
                q += self.ad[id][1]
            return q
        if s == 'b':
            for id in self.bp[p]:
                q += self.bd[id][1]
            return q
