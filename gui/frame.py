import wx
import sys

packages = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
    ('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
    ('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]


class PatFrame(wx.Frame):

    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        # create menus
        menu_sys = wx.Menu()
        memu_about = wx.Menu()
        menu_quote = wx.Menu()

        # add menu item
        menu_sys.Append(1, 'E&xit')
        menu_quote.Append(2, 'F&avorite')
        memu_about.Append(3, '&Version')

        # create menubar and add item
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_sys, "&System")
        menu_bar.Append(menu_quote, "&Quote")
        menu_bar.Append(memu_about, "&About")

        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Patience!")

        # add event
        self.Bind(wx.EVT_MENU, self.on_quite, id=1)
        self.Bind(wx.EVT_MENU, self.on_quite, id=2)
        self.Bind(wx.EVT_MENU, self.on_about, id=3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'name', width=140)
        self.list.InsertColumn(1, 'place', width=130)
        self.list.InsertColumn(2, 'year', wx.LIST_FORMAT_RIGHT, 90)

        hbox.Add(self.list, 1, wx.EXPAND | wx.ALL)
        panel.SetSizer(hbox)
        self.Centre()
        self.indexmap = {}

    def on_quite(self, event):
        self.Close()

    def on_about(self, event):
        wx.MessageBox('Version:1.0.0', "Patience", wx.OK | wx.ICON_INFORMATION, self)

    def filllist(self, init, data):
        if init:
            for i in data:
                index = self.list.InsertStringItem(sys.maxint, i[0])
                self.list.SetStringItem(index, 1, i[1])
                self.list.SetStringItem(index, 2, i[2])
                self.indexmap[i[0]] = index
        else:
            for i in data:
                self.list.SetStringItem(self.indexmap[i[0]], 1, i[1])
                self.list.SetStringItem(self.indexmap[i[0]], 2, i[2])