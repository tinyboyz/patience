from quote import Quote
import ConfigParser
from ems import EMS
import asyncore
import wx


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


class Config():
    def __init__(self):
        self.stocks_list = []
        with open('patience.ini') as f:
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(f)
            stocks = config.get('favorite', 'stocks')
            self.stocks_list = stocks.split(',')


def main():
    # config = Config()
    # print config.stocks_list
    # quote = Quote('http://finance.yahoo.com/d/quotes.csv?s=000002.ss&f=snd1l1yr', config.stocks_list)
    # quote.start()
    # quote.join()
    ex = wx.App()
    Example(None)
    ex.MainLoop()

    # emspaid = EMS('202.104.236.15', 1865)
    # emspaid.test_login_ems('hz9999', 'wokao', -4)
    # emspaid.test_6077_reg_columns_quote_list(1, 91001004, 9223372036854775807)
    # asyncore.loop()


if __name__ == '__main__':
    main()