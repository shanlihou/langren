#!/usr/bin/python
#coding:utf-8
import hashlib
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re
from DBHelper import DBHelper
class WXRequest(object):
    def __init__(self):
        self.recvMsg = {}
        self.resp = None
        print 'init'
    def checkAuth(self, dictReq):
        token = 'langren'
        arr = []
        arr.append(token)
        arr.append(dictReq['timestamp'])
        arr.append(dictReq['nonce'])
        arr.sort()
        strHash  = ''.join(arr)
        sha1 = hashlib.sha1()
        sha1.update(strHash)
        strRet = sha1.hexdigest()
        if strRet == dictReq['signature']:
            return True
        else:
            return False
    def getMsg(self, strXml):
        print strXml
        fileWrite = open('post.xml', 'w')
        fileWrite.write(strXml)
        fileWrite.close()
        DOMTree = xml.dom.minidom.parse("post.xml")
        collection = DOMTree.documentElement
        self.recvMsg['fromUser'] = collection.getElementsByTagName("ToUserName")[0].childNodes[0].data
        self.recvMsg['toUser'] = collection.getElementsByTagName("FromUserName")[0].childNodes[0].data
        self.recvMsg['MsgType'] = collection.getElementsByTagName("MsgType")[0].childNodes[0].data
        self.recvMsg['Content'] = collection.getElementsByTagName("Content")[0].childNodes[0].data
        self.parseCmd(self.recvMsg['Content'])
    def parseCmd(self, strCmd):
        '''
        cmdPat = re.compile(r'^(\w+)\s')
        cmdFind = cmdPat.search(strCmd)
        if (cmdFind):
            print cmdFind.group()   
            '''
        arg =  strCmd.split()
        if arg[0] == 'bm':
            print (type(arg[1]))
            if arg[1].isdigit() and len(arg[1].decode("utf-8")) == 8:
                print 'come here'
                if (DBHelper.checkHas(self.recvMsg['toUser'], arg[1])):
                    print 'has this'
                    self.resp = '你已经报名'
                    return False
                DBHelper.addUser(self.recvMsg['toUser'], arg[1])
                num = DBHelper.getPpNum(arg[1])
                self.resp = '报名' + str(num) + '人'
        elif arg[0] == 'cx':
            if arg[1].isdigit() and len(arg[1].decode("utf-8")) == 8:
                num = DBHelper.getPpNum(arg[1])
                self.resp = '报名' + str(num) + '人'
        return True
    def defaultResponse(self, strMsg):
        if (strMsg):
            return self.makeResponse(strMsg)
        if (self.resp):
            return self.makeResponse(self.resp)
        strResp = ''
        strResp += '功能如下\n'
        strResp += '报名:bm date, (如:bm 20161207)\n'
        strResp += '查询报名人数:cx date, (如:cx 20161207)'
        return self.makeResponse(strResp)
        
    def makeResponse(self, strMsg):
        ret = "<xml>"    
        ret = ret + "<ToUserName><![CDATA[" + self.recvMsg['toUser'] + "]]></ToUserName>"
        ret = ret + "<FromUserName><![CDATA["+ self.recvMsg['fromUser'] + "]]></FromUserName>"
        strTime = str(int(time.time()))
        print strTime
        ret = ret + "<CreateTime>" + strTime + "</CreateTime>"
        ret = ret + "<MsgType><![CDATA[text]]></MsgType>"
        ret = ret + "<Content><![CDATA[" + strMsg + "]]></Content>"
        ret = ret + "</xml>"
        return ret
        