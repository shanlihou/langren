#!/usr/bin/python
#coding:utf-8
import hashlib
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re
from DBHelper import DBHelper
from game import GAME
from PCControl import PCControl
class WXRequest(object):
    def __init__(self):
        self.recvMsg = {}
        self.resp = None
        self.option = "狼:wolf\n猎人:hunt\n预言家:seer\n女巫:witch\n丘比特:cupid\n守卫:guard\n白痴:idiot\n白狼:white_wolf\n盗贼:thief\n"
#        self.option += 'enter add:进入添加人模式\n'
#        self.option += 'enter night:进入晚上\n'
#        self.option += 'enter day:天亮了\n'
        self.option += 'add 1 wolf:添加自己为1号狼\n'
        self.option += 'get all:获得人数状态\n'
        self.option += 'get mine:获得我的状态\n'
        self.option += 'get kill:女巫获得谁死了\n'
        self.option += 'get wolf:预言家获得谁是狼\n'
        self.option += 'get live:获得活着的人\n'
        self.option += 'link 1 2:1和2号成为链子\n'
        self.option += 'kill 2:狼操作，2号被刀\n'
        self.option += 'save:女巫救人\n'
        self.option += 'guard 5:守卫保护5号\n'
        self.option += 'shoot 5:猎人开枪带走5号\n'
#        self.option += 'reset:重置游戏\n'
        print 'init'
    def checkAuth(self, dictReq):
        if not dictReq.has_key("timestamp"):
            return False
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
        arg =  strCmd.lower().split()
        print 'arg0:' + arg[0]
        print 'arg1:' + arg[1]
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
                       
        elif arg[0] == 'enter':
            if (arg[1] == 'add'):
                GAME.enter(1)
                self.resp = '进入add成功'
            elif arg[1] == 'night':
                GAME.enter(2)
                self.resp = '进入黑夜'
            elif arg[1] == 'day':
                self.resp = GAME.enter(3)
            else:
                self.resp = '操作失败'
        elif arg[0] == 'add':
            if (len(arg) == 3):
                if GAME.add(self.recvMsg['toUser'], arg[1], arg[2]):
                    self.resp = '操作成功'
                else:
                    self.resp = '操作失败'
            else:
                self.resp = '操作失败'
        elif arg[0] == 'get':
            if len(arg) < 2:
                self.resp = '操作失败'
            elif arg[1] == 'all':
                self.resp = GAME.getAllUser()
            elif arg[1] == 'mine':
                self.resp = GAME.getMine(self.recvMsg['toUser'])
            elif arg[1] == 'kill':
                self.resp = '死的是' + str(GAME.getKill(self.recvMsg['toUser'])) + '号'
            elif arg[1] == 'wolf':
                self.resp = GAME.getWolf(self.recvMsg['toUser'], arg[2])
            elif arg[1] == 'live':
                self.resp = GAME.getLive()
            elif arg[1] == 'option':
                self.resp = self.option
            else:
                self.resp = '操作失败'
        elif arg[0] == 'link':
            if len(arg) == 3:
                if GAME.link(self.recvMsg['toUser'], arg[1], arg[2]):
                    self.resp = '操作成功'
                else:
                    self.resp = '操作失败'
            else:
                self.resp = '操作失败'
        elif arg[0] == 'kill':
            if len(arg) < 2:
                self.resp = '操作失败'
            else:
                if GAME.kill(self.recvMsg['toUser'], arg[1]):
                    self.resp = '操作成功'
                else:
                    self.resp = '操作失败'     
        elif arg[0] == 'save':
            if GAME.save(self.recvMsg['toUser']):
                self.resp = '操作成功'
            else:
                self.resp = '操作失败'
        elif arg[0] == 'poison':
            if len(arg) < 2:
                self.resp = '操作失败'
            elif GAME.poison(self.recvMsg['toUser'], arg[1]):
                self.resp = '操作成功'
            else:
                self.resp = '操作失败'
        elif arg[0] == 'guard':
            if len(arg) < 2:
                self.resp = '操作失败'
            else:
                self.resp = GAME.guard(self.recvMsg['toUser'], arg[1])
        elif arg[0] == 'shoot':
            if len(arg) < 2:
                self.resp = '操作失败'
            else:
                self.resp = GAME.guard(self.recvMsg['toUser'], arg[1])
        elif arg[0] == 'reset':
            GAME.reset()
            self.resp = '操作成功'
        elif arg[0] == 'pc':
            print 'enter pc'
            if arg[1] == 'open':
                self.resp = PCControl.wantOpen()
            elif arg[1] == 'close':
                self.resp = PCControl.wantClose()
            elif arg[1] == 'isopen':
                self.resp = str(PCControl.isPCOpen())
            elif arg[1] == 'iswantopen':
                self.resp = str(PCControl.isNeedClose())
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
        