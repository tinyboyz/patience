# -*- coding: utf-8 -*-
# create by leon[zhanglei.js]
# unittest
# 2012-07-03

from base import Base
import struct
from time import localtime, strftime, time, sleep
import threading
from datetime import date
from convenience import Convenience
from ctypes import *


class EMS(Base):
    """
    some messages of the ems service
        516:  Multiple Stocks Quotation
        6003: Merged Transaction Details
        6005: Change Range
        6008: Reg Green Formula
        6018: Multiple Indexes Quotation
        6020: Subscribe Single Stock Quotation
        6022: Subscribe Merged Transaction Details By A Certain Time
        6035: Subscribe Special Quotation Events
        6046: Subscribe Single Stock Quotation Level2
        6055: Heart beat
        6075: Subscribe Single Stock Trend Line
        6077: Subscribe Custom Columns Quotation List
        6078: Subscribe Capital Flows List
    """

    def __init__(self, ip, port):
        Base.__init__(self, ip, port)
        self.timer_bh = threading.Timer(60.0, self.test_6055_beatheart)
        self.pylcm = cdll.LoadLibrary('pylcm')
        self.pylcm.create_instance()
        self.stocks = {}  # all stocks

    def __del__(self):
        self.pylcm.free_instance()

    def test_login_ems(self, username, password, clienttype):
        """测试登录EMS"""
        lstusername = []
        lstpassword = []
        for u in username:
            lstusername.append(ord(u))
        for p in password:
            lstpassword.append(ord(p))
        lstusername = lstusername + [0] * (32 - len(lstusername))
        lstpassword = lstpassword + [0] * (32 - len(lstpassword))
        lst = [0, 0, 0, 0]
        list1 = lstusername + lst + lstpassword
        self.sendbuf += struct.pack("=ihiiBBBBBii68B", 81, 609, 0, 0, 4, 0, 0, 0, 0, 0, clienttype, *list1)
        self.make_a_tag(self.sendaction, 609, 95)

    def test_stock_dict(self, savefile):
        """测试码表接口"""
        print "[stock dict]"
        #list2 = [0x00,0x33,0x30,0x30,0x30,0x35,0x39,0x00,0x02]
        list1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        list2 = [0x69, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        list3 = [0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        list4 = [0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        strsendbuf1 = struct.pack("=ihiii34B", 140, 715, 0, 0, 4, *list1)
        strsendbuf2 = struct.pack("=34B", *list2)
        strsendbuf3 = struct.pack("=34B", *list3)
        strsendbuf4 = struct.pack("=34B", *list4)
        strsendbuf = strsendbuf1 + strsendbuf2 + strsendbuf3 + strsendbuf4
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            validnum, = struct.unpack("=i", body[:4])
            origsize, comprsize, = struct.unpack("=ii", body[38:46])
            #quotedate,time,high,low,close,offsetpre,offset,rtminpre,rtmin = struct.unpack("=iifffHHHH", body[8:36])
            print "[validnum:%d]" % validnum
            print "[origsize:%d]" % origsize
            print "[comprsize:%d]" % comprsize
            if savefile == 1:
                f = open('e:\\scratch\\tmp.txt', 'wb')
                f.write(body[4:])
                f.close()
                #print "[date:%d]" % quotedate
                #print "[time:%d]" % time
                #print "[high:%f]" % high
                #print "[low:%f]" % low
                #print "[close:%f]" % close
                #print "[offsetpre:%d]" % offsetpre
                #print "[offset:%d]" % offset
                #print "[rtminpre:%d]" % rtminpre
                #print "[rtmin:%d]" % rtmin

    def test_old_trend_line(self):
        """测试旧的分时走势接口"""
        print "[trend line][399001]"
        #list2 = [0x00,0x33,0x30,0x30,0x30,0x35,0x39,0x00,0x02]
        #list= [0x00,0x33,0x39,0x39,0x30,0x30,0x31,0x00,0x02]
        list = [0x01, 0x36, 0x30, 0x30, 0x30, 0x30, 0x30, 0x00, 0x02]
        strsendbuf = struct.pack("=ihiiii9B", 17, 3018, 0, 0, 0, 0, *list)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            quotedate, time, high, low, close, offsetpre, offset, rtminpre, rtmin = struct.unpack("=iifffHHHH",
                                                                                                  body[8:36])
            print "[date:%d]" % quotedate
            print "[time:%d]" % time
            print "[high:%f]" % high
            print "[low:%f]" % low
            print "[close:%f]" % close
            print "[offsetpre:%d]" % offsetpre
            print "[offset:%d]" % offset
            print "[rtminpre:%d]" % rtminpre
            print "[rtmin:%d]" % rtmin
            _offset = 0
            for i in range(0, rtminpre + rtmin):
                price, volumn, averprice, = struct.unpack("=fif", body[36 + _offset:48 + _offset])
                _offset += 12
                print "[{}][{:.2f}][{}][{:.2f}]".format(i, price, volumn, averprice)

    def test_old_trend_line_sif(self):
        """测试旧的分时走势股指期货接口"""
        print "[trend line][040120]"
        strsendbuf = struct.pack("=ihiiiiH", 10, 3019, 0, 0, 16795656, 0, 0)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            quotedate, index, time, open, high, low, close, volume, value1, value2, rtmin, = struct.unpack(
                "=iHiffffiiiH", body[4:44])
            print "[date:%d]" % quotedate
            print "[index:%d]" % index
            print "[time:%d]" % time
            print "[open:%f]" % open
            print "[high:%f]" % high
            print "[low:%f]" % low
            print "[close:%f]" % close
            print "[volume:%d]" % volume
            print "[rtmin:%d]" % rtmin
            j = 0
            i = 0
            for i in range(0, rtmin - 1):
                price, volume, temp1, temp2 = struct.unpack("=fifi", body[44 + j:60 + j])
                print "[%d][%d][price:%f][volume:%d]" % (i, j, price, volume)
                j = j + 16

    def test_trend_line(self, msgid, savefile):
        """测试相同style相同container的不同股票的覆盖注册功能"""
        print "[trend line][same style and same containter]"
        print "[1]===========[style1,con805340160(64)]"
        strsendbuf = struct.pack("=ihiiBIBIBII", 19, msgid, 0, 0, 1, 1, 1, 805340160, 1, 402653185, 0)
        self._test_trend_line(strsendbuf, savefile)

    def _test_trend_line(self, strsendbuf, savefile):
        """test new trend line & trend line capital flows"""
        print "[req bytes:%d]" % len(strsendbuf)
        bret = self.rs.send(strsendbuf)
        if bret:
            while True:
                bret = self.rs.recv_analyze()
                if bret:
                    result = self.rs.getresult()
                    body = self.rs.getbody()
                    if result == 0:
                        errid, = struct.unpack("=h", body[:2])
                        print "[errid:%d]" % errid
                        break
                    if result == 1:
                        incrementid, pushstat, stocknum, datalen, = struct.unpack("=iBHi", body[:11])
                        if savefile == 1:
                            f = open('e:\\scratch\\tmp.txt', 'wb')
                            f.write(body[11:])
                            f.close()
                        if pushstat == 0:
                            print "[incrementid:%d]" % incrementid
                            print "[pushstat:%d]" % pushstat
                            print "[stocknum:%d]" % stocknum
                            print "[datalen:%d]" % datalen
                        if pushstat == 1 or pushstat == 2:
                            print "[incrementid:%d]" % incrementid
                            print "[pushstat:%d]" % pushstat
                            print "[stocknum:%d]" % stocknum
                            print "[datalen:%d]" % datalen
                            break
                else:
                    break

    def test_trend_line_same_style_diff_container(self, msgid):
        """测试相同style不同container的注册功能"""
        print "[trend line][same style & diff container]"
        print "[1][style0,con0(64,128),con1(1),con2(65,402653185,402653249)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIIIBIIIBIIIIII", 69, msgid, 0, 0, 1, 0, 3, 0, 2, 64, 0, 128, 0, 1, 1, 1,
                                 0, 2, 3, 65, 0, 402653185, 0, 402653249, 0)
        self._test_trend_line(strsendbuf)

        print "[2][style0,con0(64,128),con2(201332736),con3(201332288)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIIIBIIIBII", 53, msgid, 0, 0, 1, 0, 3, 0, 2, 64, 0, 128, 0, 2, 1,
                                 201332736, 0, 3, 1, 201332288, 0)
        self._test_trend_line(strsendbuf)

    def test_trend_line_diff_style(self, msgid):
        """测试不同style的全部覆盖注册功能"""
        print "[trend line][diff style]"
        print "[1]===========[style1,con0(256),con2(64,128,256)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIBIIIIII", 48, msgid, 0, 0, 1, 1, 2, 0, 1, 256, 0, 2, 3, 64, 0, 128, 0,
                                 192, 0)
        self._test_trend_line(strsendbuf)

        print "[2]===========[style5,con0(),con2(320)]"
        strsendbuf = struct.pack("=ihiiBIBIBIBII", 24, msgid, 0, 0, 1, 5, 2, 0, 0, 2, 1, 320, 0)
        self._test_trend_line(strsendbuf)

    def test_trend_line_same_style_same_container(self, msgid):
        """测试相同style相同container的不同股票的覆盖注册功能"""
        print "[trend line][same style and same containter]"
        print "[1]===========[style1,con805340160(64)]"
        strsendbuf = struct.pack("=ihiiBIBIBII", 19, msgid, 0, 0, 1, 1, 1, 805340160, 1, 64, 0)
        self._test_trend_line(strsendbuf)

        print "[2]===========[style1,con805340160(128)]"
        strsendbuf = struct.pack("=ihiiBIBIBII", 19, msgid, 0, 0, 1, 1, 1, 805340160, 1, 128, 0)
        self._test_trend_line(strsendbuf)

        print "[3]===========[style1,con805340160(256)]"
        strsendbuf = struct.pack("=ihiiBIBIBII", 19, msgid, 0, 0, 1, 1, 1, 805340160, 1, 256, 0)
        self._test_trend_line(strsendbuf)

    def test_trend_line_certain_time(self, msgid):
        """测试一段时间获取分时数据的功能"""
        today = date.today()
        strtoday = today.strftime("%y%m%d1038")
        print "[trend line][%s 10:38]" % strtoday
        print "[1][style0,con0(128)]"
        strsendbuf = struct.pack("=ihiiBIBIBII", 19, msgid, 0, 0, 1, 0, 1, 0, 1, 128, int(strtoday))
        self._test_trend_line(strsendbuf)

    def test_trend_line_max_container(self, msgid):
        """测试一个container中最大可以注册的股票数量的功能"""
        print "[trend line][max container]"
        print "[1][style1,con0(402653441,402653505,402653569,402653633,402653697,402653761,402654209,402654273,402654337,402654401,402654465,402654529,402654593,402654657,402654721,402654785,402655233,402655297,402655361,402655617,402655681,402655745,402655809,402656257)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII", 203, msgid, 0, 0, 1, 1,
                                 1, 0, 24, 402653441, 0, 402653505, 0, 402653569, 0, 402653633, 0, 402653697, 0,
                                 402653761, 0, 402654209, 0, 402654273, 0, 402654337, 0, 402654401, 0, 402654465, 0,
                                 402654529, 0, 402654593, 0, 402654657, 0, 402654721, 0, 402654785, 0, 402655233, 0,
                                 402655297, 0, 402655361, 0, 402655617, 0, 402655681, 0, 402655745, 0, 402655809, 0,
                                 402656257, 0)
        self._test_trend_line(strsendbuf)

    def test_trend_line_same_style_diff_container2(self, msgid):
        """测试当每次注册相同style不同container时，container的累加状况，以及超过最大容器限制时的处理状况"""
        print "[trend line][same style & diff container 2]"
        print "[1][style1,con0(402653441),con1(402653569),con2(402653697),con3(402654209),con4(402654337),con5(402654465),con6(402654593),con7(402654721),con8(402655233),con9(402655361),con10(402655681)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBII", 149, msgid, 0, 0, 1, 1, 11, 0,
                                 1, 402653441, 0, 1, 1, 402653569, 0, 2, 1, 402653697, 0, 3, 1, 402654209, 0, 4, 1,
                                 402654337, 0, 5, 1, 402654465, 0, 6, 1, 402654593, 0, 7, 1, 402654721, 0, 8, 1,
                                 402655233, 0, 9, 1, 402655361, 0, 10, 1, 402655681, 0)
        self._test_trend_line(strsendbuf)

        print "[2][style1,con0(402653505),con11(402653633),con12(402653761),con13(402654273),con14(402654401),con15(402654529),con16(402654657),con17(402654785),con18(402655297),con19(402655617),con20(402655745),con21(64)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBII", 162, msgid, 0, 0, 1, 1, 12,
                                 0, 1, 402653505, 0, 11, 1, 402653633, 0, 12, 1, 402653761, 0, 13, 1, 402654273, 0, 14,
                                 1, 402654401, 0, 15, 1, 402654529, 0, 16, 1, 402654657, 0, 17, 1, 402654785, 0, 18, 1,
                                 402655297, 0, 19, 1, 402655617, 0, 20, 1, 402655745, 0, 21, 1, 64, 0)
        self._test_trend_line(strsendbuf)

        print "[3][style1,con0(402653633),con22(65),con23(128),con24(402653185),con25(402653249),con26(402654401),con27(402654529),con28(402654593),con29(402655297),con30(402655233),con31(402655745),con32(402654721)]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBIIIBII", 162, msgid, 0, 0, 1, 1, 12,
                                 0, 1, 402653633, 0, 22, 1, 65, 0, 23, 1, 128, 0, 24, 1, 402653185, 0, 25, 1, 402653249,
                                 0, 26, 1, 402654401, 0, 27, 1, 402654529, 0, 28, 1, 402654593, 0, 29, 1, 402655297, 0,
                                 30, 1, 402655233, 0, 31, 1, 402655745, 0, 32, 1, 402654721, 0)
        self._test_trend_line(strsendbuf)

    def test_batch_reg_columns_quote_list(self):
        """
        批量测试定制字段行情列表
        """
        print "[batch custom columns quotation list]"
        f = open('e:\\scratch\\blocklist2', 'r')
        fresult = open('e:\\scratch\\blcoklist2_result', 'w')
        for line in f:
            li = line.split(',')
            if self.test_6077_reg_columns_quote_list(0, 5, 6077, int('91' + li[0]), 9223372036854775807):
                fresult.write('{0},{1}\n'.format(li[0], 'ok'))
            else:
                fresult.write('{0},{1}\n'.format(li[0], 'failed'))
            sleep(1)
        fresult.close()
        f.close()

    def test_block_cfs_detail(self):
        """测试板块资金流详细列表接口"""
        print "[block cfs detail]"
        #list2 = [0x00,0x33,0x30,0x30,0x30,0x35,0x39,0x00,0x02]
        list = [0x00, 0x33, 0x39, 0x39, 0x30, 0x30, 0x31, 0x00, 0x02]
        strsendbuf = struct.pack("=ihiibb", 2, 628, 0, 0, 1, -1)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            datasize, = struct.unpack("=i", body[6:10])
            print "[datasize:%d]" % datasize
            #f = open('tmp', 'w')
            #f.write(body[10:])
            #f.close()

    def test_stock_cfs_detail(self):
        """测试板块个股资金流详细列表接口"""
        print "[stock cfs detail]"
        #list2 = [0x00,0x33,0x30,0x30,0x30,0x35,0x39,0x00,0x02]
        list = [0x00, 0x33, 0x39, 0x39, 0x30, 0x30, 0x31, 0x00, 0x02]
        strsendbuf = struct.pack("=ihiibb", 2, 635, 0, 0, 1, 3)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            datasize, = struct.unpack("=i", body[6:10])
            print "[datasize:%d]" % datasize
            #f = open('tmp', 'w')
            #f.write(body[10:])
            #f.close()

    def test_sob_cfs_detail(self):
        """测试板块个股资金流详细列表接口"""
        print "[sob cfs detail]"
        #list2 = [0x00,0x33,0x30,0x30,0x30,0x35,0x39,0x00,0x02]
        list = [0x00, 0x33, 0x39, 0x39, 0x30, 0x30, 0x31, 0x00, 0x02]
        strsendbuf = struct.pack("=ihiibi", 5, 632, 0, 0, 1, 17661997)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            datasize, = struct.unpack("=i", body[9:13])
            print "[datasize:%d]" % datasize
            #f = open('tmp', 'w')
            #f.write(body[10:])
            #f.close()

    def test_sif_quotation(self):
        """测试股指期货行情数据"""
        print "[sif quotation]"
        strsendbuf = struct.pack("=ihiiBBI", 6, 812, 0, 0, 5, 1, 16795656)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            header = self.rs.gethead()
            bodylen, = struct.unpack("=I", header[:4])
            print "[bodylen:%d]" % bodylen

    def test_nlevel(self):
        """测试百档行情数据"""
        print "[nlevel]"
        strsendbuf = struct.pack("=ihiiBIBIBIIIBIIBIII", 45, 817, 0, 0, 1, 0, 3, 0, 2, 64, 128, 1, 1, 256, 2, 3, 256,
                                 320, 384)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            head = self.rs.gethead()
            bodylen, msgid, = struct.unpack("=IH", head[:6])
            body = self.rs.getbody()
            incid, status, size = struct.unpack("=IBB", body[:6])
            if size == 0:
                print "[%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d]" % (
                    strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, incid, status, size)
            else:
                print "[%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d]" % (
                    strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, incid, status, size),
            for i in range(size):
                sid, datalen, = struct.unpack("=II", body[6 + dataoffset:14 + dataoffset])
                dataoffset = dataoffset + 8 + datalen
                if i == size - 1:
                    print "[sid:%d][datalen:%d]" % (sid, datalen)
                else:
                    print "[sid:%d][datalen:%d]" % (sid, datalen),

    def test_nlevel_jj(self):
        """测试百档行情数据"""
        print "[nlevel_JJ]"
        strsendbuf = struct.pack("=ihiiBBIII", 14, 6071, 0, 0, 1, 3, 256, 320, 384)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            head = self.rs.gethead()
            bodylen, msgid, = struct.unpack("=IH", head[:6])
            body = self.rs.getbody()
            incid, status, size = struct.unpack("=IBB", body[:6])
            print "[%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d]" % (
                strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, incid, status, size),
            dataoffset = 0
            for i in range(size):
                sid, datalen, = struct.unpack("=II", body[6 + dataoffset:14 + dataoffset])
                dataoffset = dataoffset + 8 + datalen
                if i == size - 1:
                    print "[sid:%d][datalen:%d]" % (sid, datalen)
                else:
                    print "[sid:%d][datalen:%d]" % (sid, datalen),

    def test_if_usage_stat(self):
        """测试统计接口调用情况"""
        print "[interface usage statistics]"
        strsendbuf = struct.pack("=ihii", 0, 6076, 0, 1)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            dataoffset = 0
            size, = struct.unpack("=I", body[:4])
            print "[size:%d]" % size
            for i in range(size):
                msgid, times = struct.unpack("=II", body[dataoffset + 4:dataoffset + 12])
                dataoffset = dataoffset + 8
                print "[msgid:%d][times:%d]" % (msgid, times)

    def test_nlevel_qrder_queue_jj(self):
        """测试百档委托队列行情数据"""
        print "[nlevel order queue JJ]"
        strsendbuf = struct.pack("=ihii BB IfBIfB", 20, 6072, 0, 0, 1, 2, 64, 11.38, 1, 128, 9.59, 0)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            head = self.rs.gethead()
            bodylen, msgid, = struct.unpack("=IH", head[:6])
            body = self.rs.getbody()
            incid, status, size = struct.unpack("=IBB", body[:6])
            #incid,status,size,sid,price,type,datalen, = struct.unpack("=IBBIfBI", body[:19])
            if size == 0:
                print "[%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d]" % (
                    strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, incid, status, size)
            else:
                print "[%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d]" % (
                    strftime('%Y-%m-%d %H:%M:%S'), msgid, bodylen, incid, status, size),
            dataoffset = 0
            for i in range(size):
                sid, price, type, datalen, = struct.unpack("=IfBI", body[6 + dataoffset:19 + dataoffset])
                dataoffset = dataoffset + 13 + datalen
                if i == size - 1:
                    print "[sid:%d][price:%f][type:%d][datalen:%d]" % (sid, price, type, datalen)
                else:
                    print "[sid:%d][price:%f][type:%d][datalen:%d]" % (sid, price, type, datalen),

    def test_nlevel_qrder_queue(self):
        """测试百档委托队列行情数据"""
        print "[nlevel order queue]"
        strsendbuf = struct.pack("=ihii BIB IBIfBIfB IBIfB IBIfBIfBIfB", 75, 818, 0, 0, 1, 0, 3, 0, 2, 64, 14.31, 1,
                                 128, 9.28, 1, 1, 1, 256, 7.47, 1, 2, 3, 256, 2.7, 1, 320, 4.22, 0, 384, 13.14, 0)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            incid, status, size = struct.unpack("=IBB", body[:6])
            print "[%s][msgid:818][size:%d][status:%d][incrementid:%d][bodylen:%d]" % (
                strftime('%Y-%m-%d %H:%M:%S'), size, status, incid, len(body))

    def test_nlevel_same_style_same_container(self):
        """测试相同style相同container的不同股票的覆盖注册功能"""
        print "[nlevel][same style and same containter]"
        print "[1]===========[style1,con805340160(64)]"
        strsendbuf = struct.pack("=ihiiBIBIBI", 15, 819, 0, 0, 1, 1, 1, 805340160, 1, 64)
        self.rs.send(strsendbuf)

        print "[2]===========[style1,con805340160(128)]"
        strsendbuf = struct.pack("=ihiiBIBIBI", 15, 819, 0, 0, 1, 1, 1, 805340160, 1, 128)
        self.rs.send(strsendbuf)

        print "[3]===========[style1,con805340160(256)]"
        strsendbuf = struct.pack("=ihiiBIBIBI", 15, 819, 0, 0, 1, 1, 1, 805340160, 1, 256)
        self.rs.send(strsendbuf)

    def test_order_push(self):
        """"""
        print "[order queue]"
        strsendbuf = struct.pack("=ihiiIB", 5, 803, 0, 0, 64, 1)
        bret = self.rs.send_recv_analyze(strsendbuf)
        if bret:
            body = self.rs.getbody()
            num, = struct.unpack("=B", body[4:6])
            print "[%s][msgid:803][num:%d]" % (strftime('%Y-%m-%d %H:%M:%S'), num)

    def test_516_multi_stocks_quote(self):
        self.sendbuf += struct.pack("=ihiiBBII", 10, 516, 0, 0, 1, 2, 402653185, 64)
        self.make_a_tag(self.sendaction, 516, 24)

    def test_6003_merged_transaction_details(self, market, code):
        self.sendbuf += struct.pack("=ihiiIIIB7s", 20, 6003, 0, 0, Convenience.time_to_int_date(), 0, 0, market, code)
        self.make_a_tag(self.sendaction, 6003, 34)

    def test_6005_change_range(self, stocktype, min5_or_day):
        """
        stocktype(interger): NLBM_SHAG(2), NLBM_SHJJ(9), NLBM_SHBG(7), NLBM_SHZS(5), NLBM_SHZQ(8)
        min5_or_day(integer): min5(1), day(0)
        """
        self.sendbuf += struct.pack("=ihiiBB", 2, 6005, 0, 0, stocktype, min5_or_day)
        self.make_a_tag(self.sendaction, 6005, 16)

    def test_6008_red_green_formula(self, market, code):
        self.sendbuf += struct.pack("=ihiiIIB7s", 16, 6008, 0, 0, Convenience.time_to_int_date(), 0, market, code)
        self.make_a_tag(self.sendaction, 6008, 30)

    def test_6018_multi_indexes_quote(self):
        self.sendbuf += struct.pack("=ihiiBBII", 10, 6018, 0, 0, 1, 2, 241434689, 65)
        self.make_a_tag(self.sendaction, 6018, 24)

    def test_6020_sub_single_stock_quote(self, market, code):
        self.sendbuf += struct.pack("=ihiiB7sB", 9, 6020, 0, 0, market, code, 1)
        self.make_a_tag(self.sendaction, 6020, 23)

    def test_6022_sub_merged_transaction_details_by_time(self, market, code):
        self.sendbuf += struct.pack("=ihiiB7sBI", 13, 6022, 0, 0, market, code, 2, 5)
        self.make_a_tag(self.sendaction, 6022, 27)

    def test_6035_sub_special_quote_events(self):
        self.sendbuf += struct.pack("=ihiiBBIIII", 18, 6035, 0, 0, 0, 1, 0, 16383, 0, 5)
        self.make_a_tag(self.sendaction, 6035, 32)

    def test_6046_single_stock_quote_l2(self, stockid):
        self.sendbuf += struct.pack("=ihiiIB", 5, 6046, 0, 0, stockid, 1)
        self.make_a_tag(self.sendaction, 6046, 19)

    def test_6055_beatheart(self):
        self.sendbuf += struct.pack("=ihii", 0, 6055, 0, 0)
        self.make_a_tag(self.sendaction, 6055, 14)
        self.timer_bh = threading.Timer(60.0, self.test_6055_beatheart)
        self.timer_bh.start()

    def test_6062_sub_single_stock_trendline(self, market, code):
        self.sendbuf += struct.pack("=ihiiIIB7sB", 17, 6062, 0, 0, 0, 0, market, code, 2)
        self.make_a_tag(self.sendaction, 6062, 31)

    def test_6074_multi_stocks_quote_20s(self, stockid):
        self.sendbuf += struct.pack("=ihiiBBI", 6, 6074, 0, 0, 1, 1, stockid)
        self.make_a_tag(self.sendaction, 6074, 20)

    def test_6075_single_stock_trendline(self, stockid):
        self.sendbuf += struct.pack("=ihiiBII", 9, 6075, 0, 0, 1, stockid, 0)
        self.make_a_tag(self.sendaction, 6075, 23)

    def test_6077_reg_columns_quote_list(self, reg, categoryid, columns):
        self.sendbuf += struct.pack("=ihiiBQBQ", 18, 6077, 0, 0, reg, categoryid, 1, columns)
        self.make_a_tag(self.sendaction, 6077, 32)

    def test_6078_capital_flows_list(self, reg, typeid, categoryid):
        self.sendbuf += struct.pack("=ihiiBBQ", 10, 6078, 0, 0, reg, typeid, categoryid)
        self.make_a_tag(self.sendaction, 6078, 24)

    def handle_connect(self):
        Base.handle_connect(self)
        self.timer_bh.start()

    def handle_close(self):
        Base.handle_close(self)
        self.timer_bh.cancel()

    def handle_read(self):
        """
            handle read data
        """
        Base.handle_read(self)
        self.recvbuf += self.recv(8192)
        recvbuflen = len(self.recvbuf)
        if recvbuflen >= self.headerlen:
            bodylen, msgid, ownerid, result, encrypt, compress, magicid = struct.unpack("=ihiBBBi",
                                                                                        self.recvbuf[:self.headerlen])
            if recvbuflen >= self.headerlen + bodylen:
                body = self.recvbuf[self.headerlen:self.headerlen + bodylen]
                if result == 0:
                    errid, = struct.unpack("=h", body[:2])
                    self.make_a_tag(self.recvaction, msgid, bodylen, '[errid:{0}]'.format(errid))
                else:
                    strtime = strftime('%Y-%m-%d %H:%M:%S')
                    if msgid == 516:
                        self.make_a_tag(self.recvaction, msgid, bodylen)
                        offset = 1
                        num, = struct.unpack("=B", body[:1])
                        for i in range(0, num):
                            market, timelastsale, code, = struct.unpack("=BI6s", body[offset:offset + 11])
                            offset += 141
                            print "\t[{0}][{1}][{2}]".format(market, code, timelastsale)
                    elif msgid == 609:
                        self.make_a_tag(self.recvaction, msgid, bodylen)
                    elif msgid == 6005:
                        min5_or_day, stocktype, = struct.unpack("=BB", body[:2])
                        self.make_a_tag(self.recvaction, msgid, bodylen,
                                        '[{0}][{1}]'.format({1: 'min5', 0: 'day'}[min5_or_day],
                                                            {2: 'ag',
                                                             7: 'bg',
                                                             9: 'jj',
                                                             5: 'zs',
                                                             8: 'zq'}[stocktype]))
                        offset = 2
                        for i in range(0, 20):
                            for j in range(0, 4):
                                code, name, pre_close, price, volumn, value, = struct.unpack(
                                    "=7s9sffIf",
                                    body[offset+j*20*32:offset+j*20*32+32])
                                print u'\t{0}\t{1:.2f}\t{2:.2f}%'.format(name.decode('cp936'), price,
                                                                         abs(price-pre_close)/pre_close*100),
                                if j == 3:
                                    print ''
                            offset += 32
                    elif msgid == 6008:
                        num, = struct.unpack("=H", body[11:13])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}]'.format(num))
                    elif msgid == 6018:
                        num, = struct.unpack("=B", body[:1])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}]'.format(num))
                    elif msgid == 6020:
                        timelastsale, = struct.unpack("=I", body[9:13])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}]'.format(timelastsale))
                    elif msgid == 6022:
                        offset = 12
                        num, = struct.unpack("=I", body[8:12])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}]'.format(num))
                        for i in range(0, num):
                            hr, mi, se, bs, pri, vol, trades, = struct.unpack("=BBBBIIH", body[offset:offset + 14])
                            offset += 14
                            print "\t[{0:02d}:{1:02d}:{2:02d}][{3}][{4}][{5}][{6}]".format(hr, mi, se, bs, pri, vol,
                                                                                           trades)
                    elif msgid == 6035:
                        num, = struct.unpack("=I", body[1:5])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}]'.format(num))
                        offset = 5
                        for i in range(0, num):
                            stype, mtype, ti, sid, stockid, msglen, = struct.unpack("=BIIIIH", body[offset:offset + 19])
                            offset += 19
                            msg, = struct.unpack("={0}s".format(msglen), body[offset:offset + msglen])
                            print "\t[{0}][{1}][{2}][{3}][{4}]".format(ti, stype, mtype, stockid, msg)
                            offset += (msglen + 1)
                    elif msgid == 6046:
                        timeoflastsale, = struct.unpack("=I", body[1:5])
                        self.make_a_tag(self.recvaction, msgid, bodylen,
                                        '[{0}]'.format(Convenience.time_to_string(timeoflastsale)))
                    elif msgid == 6055:
                        serverdate, servertime = struct.unpack("=II", body[:8])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0},{1}]'.format(serverdate, servertime))
                    elif msgid == 6062:
                        offset = 36
                        seq = 1
                        market, code, = struct.unpack("=B7s", body[:8])
                        pre_num, num, = struct.unpack("=HH", body[32:36])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}:{1}][{2},{3}]'.format(market, code,
                                                                                                     pre_num, num))
                        for i in range(0, num):
                            pri, vol, avgpri, = struct.unpack("=fIf", body[offset:offset + 12])
                            print "\t[{0}][{1:.2f}][{2}][{3:.2f}]".format(seq, pri, vol, avgpri)
                            offset += 12
                            seq += 1
                        seq = 1
                        for i in range(0, pre_num):
                            pri, vol, avgpri, = struct.unpack("=fIf", body[offset:offset + 12])
                            print "\t[pre{0}][{1:.2f}][{2}][{3:.2f}]".format(seq, pri, vol, avgpri)
                            offset += 12
                            seq += 1
                    elif msgid == 6071 or msgid == 6074:
                        incid, pshstat, num, dummy, datalen= struct.unpack("=IBBII", body[:14])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[{0}][{1}][{2}]'.format(incid, pshstat, num))
                        p = create_string_buffer(8192)
                        c_s = c_char_p(body[14:14 + datalen])
                        self.pylcm.uncompress_quoterec_new(c_s, datalen, p)
                        market, timeoflastsale, code, = struct.unpack('=BI7s', p[4:16])
                        print '----{0},{1},{2}'.format(market, timeoflastsale, code)
                        #f = open('e:\\scratch\\tmp.txt', 'wb')
                        #f.write(body[14:14+datalen])
                        #f.close()
                    elif msgid == 6072:
                        incid, pshstat, size, sid, price, type, datalen, = struct.unpack("=IBBIfBI", body[:19])
                        print "[%d][%s][msgid:%d][bodylen:%d][incid:%d][status:%d][size:%d][sid:%d][price:%f][type:%d]" \
                              "[datalen:%d]" % (self.recvseq, strtime, msgid, bodylen, incid, pshstat, size,
                                                sid, price, type, datalen)
                    elif msgid == 6077:
                        incid, pshstat, compresslen, = struct.unpack("=iBi", body[:9])
                        self.make_a_tag(self.recvaction, msgid, bodylen, '[increamentid:{0},pushstat:{1},'
                                                                         'compresslen:{2}]'.format(incid, pshstat,
                                                                                                   compresslen))

                        c_out_buf = create_string_buffer(10*1024*1024)
                        # c_col_buf = create_string_buffer(10*1024*1024)
                        c_in_buf = c_char_p(body[9:9 + compresslen])
                        out_buf_len = c_int()
                        col_buf_len = c_int()
                        c_out_buf = c_char_p()
                        c_col_buf = c_char_p()
                        snap = c_bool()
                        # c_out_buf = c_void_p()
                        self.pylcm.uncompress_qtlistrecjg(c_in_buf, compresslen, byref(c_out_buf), byref(out_buf_len),
                                                          byref(c_col_buf), byref(col_buf_len), byref(snap))

                        data_buf = create_string_buffer(out_buf_len.value)
                        col_buf = create_string_buffer(col_buf_len.value)
                        memmove(data_buf, c_out_buf, out_buf_len.value)
                        memmove(col_buf, c_col_buf, col_buf_len.value)
                        for i in range(0, col_buf_len.value, 2):
                            col, = struct.unpack('=H', col_buf[i:i+2])
                            print col,
                        j = 1
                        if snap.value:
                            self.stocks.clear()
                        for i in range(0, out_buf_len.value, 345):
                            stockid, = struct.unpack('=I', data_buf[i:i+4])
                            lastprice, = struct.unpack('=f', data_buf[i+20:i+24])
                            _52_week_high, _52_week_low, = struct.unpack('=ff', data_buf[i+173:i+181])
                            # print '[{0}]{1},{2:.2f},{3:.2f},{4:.2f}'.format(j, stockid, lastprice,
                            #                                                 _52_week_high, _52_week_low)
                            j += 1
                            self.stocks[stockid] = [lastprice, _52_week_high, _52_week_low]
                        print out_buf_len, col_buf_len, snap, out_buf_len.value, self.stocks
                        # market, timeoflastsale, code, = struct.unpack('=BI7s', c_out_buf[4:16])
                        # print '----{0},{1},{2}'.format(market, timeoflastsale, code)
                        # f = open('e:\\scratch\\tmp_{0}_{1}.txt'.format(msgid, self.recvseq), 'wb')
                        # f.write(body[9:])
                        # f.close()
                    else:
                        self.make_a_tag(self.recvaction, msgid, bodylen)
                self.recvbuf = self.recvbuf[self.headerlen + bodylen:]
            else:
                pass
        else:
            pass