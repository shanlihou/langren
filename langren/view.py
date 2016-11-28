from django.http import HttpResponse
from django.shortcuts import render

def langren(request):
	return HttpResponse("Hello langren ! ")

def root(request):
	return HttpResponse("Hello root ! ")

def hello(request):
    context = {}
    context['hello'] = 'Hello world!'
    return render(request, 'hello.html', context)