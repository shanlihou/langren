from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from WXRequest import WXRequest
from PCControl import PCControl
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf-8')
def langren(request):
	return HttpResponse("Hello langren ! ")

def control(dictReq):
	print('control enter')
	if dictReq.has_key('pcOpen'):
		return HttpResponse(PCControl.pcOpen())		
	elif dictReq.has_key('pcClose'):
		return HttpResponse(PCControl.pcClose())
	elif dictReq.has_key('isNeedClose'):
		return HttpResponse(PCControl.isNeedClose())
	return HttpResponse("false")
	

@csrf_exempt
def root(request):
	logger = logging.getLogger("mylogger")
	logger.debug("hello")
	wxReq = WXRequest()
	print request.method
	print request.FILES
	dictReq = request.GET
	print dictReq
	if request.get_full_path().startswith('/control?'):
		return control(dictReq)
		
	if (not wxReq.checkAuth(dictReq)):
		print 'auth failed'
		return HttpResponse("false")
	
	fileWrite = open('token.txt', 'w')
	fileWrite.write(request.get_full_path())
	
	if ('echostr' in dictReq):
		return HttpResponse(dictReq['echostr'])
	
	if request.method == 'POST':	
		strRead = request.read()
		wxReq.getMsg(strRead)
		ret = wxReq.defaultResponse(None)
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