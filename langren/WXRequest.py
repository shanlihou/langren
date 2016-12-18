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
                    self.resp = '省点力气吧，你已经报过名了，不信你查下'
                    return False
                DBHelper.addUser(self.recvMsg['toUser'], arg[1])
                num = DBHelper.getPpNum(arg[1])
                self.resp = '已经' + str(num) + '个人报名了，你还在犹豫啥？'
        elif arg[0] == 'cx':
            if len(arg) > 1 and arg[1].isdigit() and len(arg[1].decode("utf-8")) == 8:
                num = DBHelper.getPpNum(arg[1])
                self.resp = '已经' + str(num) + '个人报名了，你还在犹豫啥？'
            else:
                today = time.time()
                respStr = ''
                for i in range(7):
                    strDate = time.strftime('%Y%m%d',time.localtime(today + i * 86400))
                    num = DBHelper.getPpNum(strDate)
                    respStr += strDate + ':' + str(num) + '人报名\n'
                self.resp = respStr    
                    
        elif arg[0] == 'qx':
            if arg[1].isdigit() and len(arg[1].decode("utf-8")) == 8:
                if (DBHelper.deleteUser(self.recvMsg['toUser'], arg[1])):
                    self.resp = '取消报名成功，就这么放弃了？'
                else:
                    self.resp = '别骗我了，你根本没报名'   
        return True
    def defaultResponse(self, strMsg):
        if (strMsg):
            return self.makeResponse(strMsg)
        if (self.resp):
            return self.makeResponse(self.resp)
        strResp = '这种话"' + self.recvMsg['Content'] + '"你都说得出口，你还是按下面操作来吧\n'
        strResp += '功能如下\n'
        strResp += '报名:bm date, (如:bm 20161207)\n'
        strResp += '查询报名人数:cx date, (如:cx 20161207)\n'
        strResp += '查询七天内报名情况:cx, (如:cx)\n'
        strResp += '取消报名:qx date, (如:qx 20161207)\n'
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
        