# -*- coding: utf-8 -*-
# create by leon[zhanglei.js]
# unittest
# 2012-07-03

import datetime
from time import localtime, strftime, time, sleep


class Convenience:
    """
    useful functions
    """
    def __init__(self):
        pass

    @staticmethod
    def time_to_string(timestamp):
        t_tuple = localtime(timestamp)
        dt = datetime.datetime(*t_tuple[:6])
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def time_to_int_date():
        t_tuple = localtime()
        return t_tuple[0] * 10000 + t_tuple[1] * 100 + t_tuple[2]

    @staticmethod
    def int_to_dotted_ip(intip):
        octet = ''
        for exp in [3, 2, 1, 0]:
            octet = octet + str(intip / (256 ** exp)) + "."
            intip %= 256 ** exp
        return octet.rstrip('.')

    @staticmethod
    def dotted_ip_to_int(dotted_ip):
        exp = 3
        intip = 0
        for quad in dotted_ip.split('.'):
            intip += (int(quad) * (256 ** exp))
            exp -= 1
        return intip