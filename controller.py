import wx
from wx.lib.pubsub import pub
from wx import NotificationMessage
import wx.lib.agw.toasterbox as TB
from model.quotelist import QuoteList
from gui.mainframe import MainFrame
from gui.listframe import QuoteListPanel
from service.ems import EMS


class Controller:
    """
    Controller
    """
    def __init__(self, app):
        """
        init object
        """
        ### model
        self.quotelist = QuoteList()

        ### views
        # create frames
        self.mainframe = wx.Frame(None)
        # self.quoteframe = wx.Frame(self.mainframe)
        # self.collectframe = wx.Frame(self.mainframe)

        # create menus
        menu_sys = wx.Menu()
        memu_about = wx.Menu()
        menu_favorite = wx.Menu()

        self.quotelist_panel = QuoteListPanel(self.mainframe)
        self.collection_panel = QuoteListPanel(self.mainframe)
        self.quotelist_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.quotelist_panel, 1, wx.EXPAND)
        self.sizer.Add(self.collection_panel, 1, wx.EXPAND)
        self.mainframe.SetSizer(self.sizer)

        # add menu item
        menu_sys_subitem_exit = menu_sys.Append(wx.ID_ANY, 'E&xit')
        menu_fav_subitem_quotelist = menu_favorite.Append(wx.ID_ANY, '&Quotelist')
        menu_about_subitem_version = memu_about.Append(wx.ID_ANY, '&Version')

        # create menubar and add item
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_sys, "&System")
        menu_bar.Append(menu_favorite, "&Favorite")
        menu_bar.Append(memu_about, "&About")

        self.mainframe.SetMenuBar(menu_bar)
        self.mainframe.CreateStatusBar()
        self.mainframe.SetStatusText("Welcome to Patience!")

        # add event
        self.mainframe.Bind(wx.EVT_MENU, self.on_exit, menu_sys_subitem_exit)
        self.mainframe.Bind(wx.EVT_MENU, self.on_quotelist, menu_fav_subitem_quotelist)
        self.mainframe.Bind(wx.EVT_MENU, self.on_about, menu_about_subitem_version)

        # self.notifywidget = NotificationMessage('Notifications:', 'Initializing')
        toaster = TB.ToasterBox(self.mainframe, TB.TB_SIMPLE, TB.TB_CAPTION, TB.TB_ONCLICK, TB.TB_SCR_TYPE_FADE)
        # toaster.SetPopupPauseTime(3000)
        toaster.SetPopupPositionByInt(3)

        # wx.CallLater(1000, toaster.Play)

        # subscrite messages
        # pub.subscribe(self.on_quotelist_changed, 'Quotelist.update')
        pub.subscribe(self.on_nearby52low_changed, 'Quotelist.nearby52low')

        app.SetTopWindow(self.mainframe)
        self.mainframe.Maximize()
        # self.listframe.Show(False)
        # self.quotelist_panel.Hide()
        # self.quotelist_panel.Hide()
        # self.collection_panel.Hide()
        self.mainframe.Show()
        # self.notifywidget.Show(NotificationMessage.Timeout_Never)

        # connect
        self.ems = EMS('202.104.236.15', 1865, self.quotelist)
        self.ems.start()

    def __del__(self):
        # self.notifywidget.Close()
        self.ems.stop()

    def on_exit(self, event):
        self.mainframe.Close()

    def on_quotelist(self, event):
        if self.collection_panel.IsShown():
            self.collection_panel.Hide()
        if not self.quotelist_panel.IsShown():
            self.quotelist_panel.Show()
        self.mainframe.Layout()

    def on_about(self, event):
        wx.MessageBox('Version:1.0.0', "Patience", wx.OK | wx.ICON_INFORMATION, self)

    def on_quotelist_changed(self, issnap, data):
        """
        This method is the handler for "MONEY CHANGED" messages,
        which pubsub will call as messages are sent from the model.

        We already know the topic is "MONEY CHANGED", but if we
        didn't, message.topic would tell us.
        """
        self.quotelist_panel.set_content(issnap, data)

    def on_nearby52low_changed(self, issnap, nearby_52low):
        self.collection_panel.set_content(issnap, nearby_52low)
