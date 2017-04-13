#coding=utf8
import urllib2
import urllib
import itchat
from itchat.content import *
import sys  
import re
reload(sys)  
sys.setdefaultencoding('utf8')   
def post(data):
    #data=urllib.quote_plus(data)
    url = 'http://60.205.206.18/?signature=58a37c24b16f9f442d8854f44edaf85d0687183b&timestamp=1480424201&nonce=2011091517&openid=o1zOPuInKqVUN-7ILHP49CVEIIzs'
    data = '<xml><ToUserName><![CDATA[gh_2e3470ff053c]]></ToUserName><FromUserName><![CDATA[123]]></FromUserName><CreateTime>1480427536</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[' + data + ']]></Content><MsgId>6358387851629769718</MsgId></xml>'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    return response.read()

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print 'text_reply:' 
    print msg
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print 'download_files:' 
    print msg
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print 'add_friend:' 
    print msg
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    print 'groupchat_reply:' 
    print msg
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
    #recv = post(msg['Content'])
    data = msg['Content']
    print data
    print data.encode('UTF-8')
    print data.encode('GBK')
    #data = data.decode('GBK').encode('UTF-8')
    #data = data.decode('UTF-8').encode('GBK')
    #data = data.encode('GBK')
    if str.isalpha(data.encode("ascii")[0]):
        recv = post(data)
        print recv
        num = recv.index('<Content><![CDATA[')
        strTmp = '<Content><![CDATA['
        num2 = recv.index(']]></Content>')
        recv = recv[num + len(strTmp) : num2]
        if not recv.startswith('这种话'):
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], recv), msg['FromUserName'])
            

itchat.auto_login(True)
itchat.run()