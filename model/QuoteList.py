import wx
from wx.lib.pubsub import pub


class QuoteList:
    """
    Quote List Model
    """
    def __init__(self):
        self.quotelist = {}

    def update(self, issnap, items):
        if issnap:
            self.quotelist.clear()
            self.quotelist = {x[0]: x[:] for x in items}
        else:
            for i in items:
                self.quotelist[i[0]] = i[:]
        pub.sendMessage('Quotelist.update', issnap=issnap, data=items)
        self._check_nearby_52low()

    def _check_nearby_52low(self):
        nearby_52low = []
        factor = 1.05
        for k in self.quotelist:
            if 0 < self.quotelist[k][3] <= self.quotelist[k][5] * factor:
                nearby_52low.append(self.quotelist[k])
        pub.sendMessage('Quotelist.nearby52low', issnap=True, nearby_52low=nearby_52low)

