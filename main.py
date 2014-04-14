import ConfigParser
import wx
from controller import Controller

from gui.mainframe import MainFrame
from service.ems import EMS


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        wx.FutureCall(5000, self.ShowMessage)

        self.SetSize((300, 200))
        self.SetTitle('Message box')
        self.Centre()
        self.Show(True)

    def ShowMessage(self):
        wx.MessageBox('Download completed', 'Info',
            wx.OK | wx.ICON_INFORMATION)



# class MyFrame(wx.Frame):
#     def __init__(self, parent, id, title, size):
#         wx.Frame.__init__(self, parent, id, title, size)
#
#         hbox = wx.BoxSizer(wx.HORIZONTAL)
#         panel = wx.Panel(self, -1)
#
#         self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
#         self.list.InsertColumn(0, 'name', width=140)
#         self.list.InsertColumn(1, 'place', width=130)
#         self.list.InsertColumn(2, 'year', wx.LIST_FORMAT_RIGHT, 90)
#
#         for i in packages:
#             index = self.list.InsertStringItem(sys.maxint, i[0])
#             self.list.SetStringItem(index, 1, i[1])
#             self.list.SetStringItem(index, 2, i[2])
#
#         hbox.Add(self.list, 1, wx.EXPAND)
#         panel.SetSizer(hbox)
#
#         self.Centre()


# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None, id=-1, title="DownThemAll", size=(800,600))
#         frame.Show(True)
#         self.SetTopWindow(frame)
#         return True


class Config():
    def __init__(self):
        self.stocks_list = []
        with open('patience.ini') as f:
            config = ConfigParser.ConfigParser(allow_no_value=True)
            config.readfp(f)
            stocks = config.get('favorite', 'stocks')
            self.stocks_list = stocks.split(',')


class MyApp(wx.App):

    def OnInit(self):
        self.frame = MainFrame("Patience", (-1, -1), (-1, -1))
        self.frame.Maximize()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        emspaid = EMS('202.104.236.15', 1865, self.frame)
        emspaid.start()
        return True


def main():
    config = Config()
    print config.stocks_list
    # quote = Quote('http://finance.yahoo.com/d/quotes.csv?s=000002.ss&f=snd1l1yr', config.stocks_list)
    # quote.start()
    # quote.join()

    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()

if __name__ == '__main__':
    main()



# if __name__ == '__main__':
#     app = wx.App(False)
#     frame = wx.Frame(None, title="Demo with Notebook")
#     nb = wx.Notebook(frame)
#     nb.AddPage(cjlists(nb), "Absolute Positioning")
#     nb.AddPage(cjview(nb), "Page Two")
#     nb.AddPage(cjsave(nb), "Page Three")
#     frame.Show()
#     app.MainLoop()