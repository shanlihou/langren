from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from xml.dom.minidom import parse
import xml.dom.minidom
import hashlib
import time
def langren(request):
	return HttpResponse("Hello langren ! ")

def checkAuth(dictReq):
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
@csrf_exempt
def root(request):
	dictReq = request.GET
	if (not checkAuth(dictReq)):
		print 'auth failed'
		return False
	print request
	fileWrite = open('token.txt', 'w')
	fileWrite.write(request.get_full_path())
	if ('echostr' in dictReq):
		return HttpResponse(dictReq['echostr'])
	if request.method == 'POST':	
		print request.FILES
		strRead = request.read()
		print strRead
		fileWrite = open('post.xml', 'w')
		fileWrite.write(strRead)
		fileWrite.close()
		DOMTree = xml.dom.minidom.parse("post.xml")
		collection = DOMTree.documentElement
		ret = "<xml>"	
		ret = ret + "<ToUserName><![CDATA[" + dictReq["openid"] + "]]></ToUserName>"
		ret = ret + "<FromUserName><![CDATA[geyeguojiang]]></FromUserName>"
		strTime = str(int(time.time()))
		print strTime
		ret = ret + "<CreateTime>" + strTime + "</CreateTime>"
		ret = ret + "<MsgType><![CDATA[text]]></MsgType>"
		ret = ret + "<Content><![CDATA[hello]]></Content>"
		ret = ret + "</xml>"
		return HttpResponse(ret)
	if (request.FILES):
		print 'in'
		xmlContent = request.FILES['content']
		print xmlContent
	return HttpResponse("Hello root ! ")

def hello(request):
    context = {}
    context['hello'] = 'Hello world!'
    return render(request, 'hello.html', context)