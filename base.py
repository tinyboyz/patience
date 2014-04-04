# -*- coding: utf-8 -*-
# create by leon[zhanglei.js]
# unittest
# 2012-07-03

import struct
from time import localtime, strftime
import threading
import logging
import socket
import asyncore

thdstoped = 0
timer_bh = threading.Timer(0, 0)


class Base(asyncore.dispatcher):
    """
    base class of services
    """
    def __init__(self, ip, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.sendaction = 0
        self.recvaction = 1
        self.headerlen = 17
        self.recvbuf = ''
        self.sendbuf = ''
        self.sendseq = 0
        self.recvseq = 0
        self.connect((self.ip, self.port))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

    def handle_connect(self):
        asyncore.dispatcher.handle_connect(self)
        print '====={0}:{1} connection has been established====='.format(self.ip, self.port)

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        print '====={0}:{1} connection has been closed====='.format(self.ip, self.port)
        self.recvbuf = ''
        self.sendbuf = ''
        self.recvseq = 0
        self.sendseq = 0
        self.close()

    def handle_read(self):
        asyncore.dispatcher.handle_read(self)
        pass

    def writable(self):
        return len(self.sendbuf) > 0

    def handle_write(self):
        asyncore.dispatcher.handle_write(self)
        sent = self.send(self.sendbuf)
        self.sendbuf = self.sendbuf[sent:]

    def make_a_tag(self, action, msgid, bodylen, addtional=''):
        print '[{0}][{1}][{2}][{3}][{4}]{5}'.format({0: 'W', 1: 'R'}.get(action, ''),
                                                    {0: self.sendseq, 1: self.recvseq}.get(action, 0),
                                                    strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, addtional)
        if action == self.sendaction:
            self.sendseq += 1
        elif action == self.recvaction:
            self.recvseq += 1
