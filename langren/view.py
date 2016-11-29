from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import hashlib
def langren(request):
	return HttpResponse("Hello langren ! ")

@csrf_exempt
def root(request):
	dictReq = request.GET
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
	print strRet
	if (strRet == dictReq['signature']):
		fileWrite = open('token.txt', 'w')
		fileWrite.write(request.get_full_path())
		if ('echostr' in dictReq):
			return HttpResponse(dictReq['echostr'])
	return HttpResponse("Hello root ! ")

def hello(request):
    context = {}
    context['hello'] = 'Hello world!'
    return render(request, 'hello.html', context)