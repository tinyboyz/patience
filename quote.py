from httplib import HTTPException, HTTPConnection
from urlparse import urlparse
from time import sleep
from struct import pack, unpack
from threading import Thread
import urllib2


class Quote(Thread):
    """
    Quotation Center
    """
    def __init__(self, url, stocks):
        Thread.__init__(self)
        self.last_price = 0.0
        self.url = url
        self.stocks = stocks
        self.running = True
        self.data = {}

    def __del__(self):
        pass

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                url = 'http://hq.sinajs.cn/list=' + ','.join(self.stocks)
                print url
                response = urllib2.urlopen(url)
                data = response.read()
                # if self.data.has_key():
                print data.decode('cp936')
            except HTTPException as ex:
                print ex
            break
            sleep(3)