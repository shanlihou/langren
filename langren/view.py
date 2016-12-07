from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from WXRequest import WXRequest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def langren(request):
	return HttpResponse("Hello langren ! ")



@csrf_exempt
def root(request):
	wxReq = WXRequest()
	dictReq = request.GET
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