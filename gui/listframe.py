import wx
import sys


class QuoteListPanel(wx.Panel):
    """
    QuoteList Panel
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.listctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT)
        self.listctrl.InsertColumn(0, 'Stock', width=140)
        self.listctrl.InsertColumn(1, 'Market', width=140)
        self.listctrl.InsertColumn(2, 'Code', width=140)
        self.listctrl.InsertColumn(3, 'Last Price', width=130)
        self.listctrl.InsertColumn(4, '52week High', wx.LIST_FORMAT_RIGHT, 90)
        self.listctrl.InsertColumn(5, '52week Low', wx.LIST_FORMAT_RIGHT, 90)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.listctrl, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(hbox)
        self.indexmap = {}

    def set_content(self, init, content):
        if init:
            for i in content:
                index = self.listctrl.InsertStringItem(sys.maxint, str(i[0]))
                self.listctrl.SetStringItem(index, 1, '{:d}'.format(ord(i[1])))
                self.listctrl.SetStringItem(index, 2, '{:7s}'.format(i[2]))
                self.listctrl.SetStringItem(index, 3, '{:.2f}'.format(i[3]))
                self.listctrl.SetStringItem(index, 4, '{:.2f}'.format(i[4]))
                self.listctrl.SetStringItem(index, 5, '{:.2f}'.format(i[5]))
                self.indexmap[i[0]] = index
        else:
            for i in content:
                self.listctrl.SetStringItem(self.indexmap[i[0]], 1, '{:d}'.format(ord(i[1])))
                self.listctrl.SetStringItem(self.indexmap[i[0]], 2, '{:7s}'.format(i[2]))
                self.listctrl.SetStringItem(self.indexmap[i[0]], 3, '{:.2f}'.format(i[3]))
                self.listctrl.SetStringItem(self.indexmap[i[0]], 4, '{:.2f}'.format(i[4]))
                self.listctrl.SetStringItem(self.indexmap[i[0]], 5, '{:.2f}'.format(i[5]))
