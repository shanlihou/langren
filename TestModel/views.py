#!/usr/bin/python
#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

from TestModel.models import Test
# Create your views here.
def testdb(request):
    listDB = Test.objects.all()
    response = ''
    for i in listDB:
        print i
        response += i.name + ' '
    return HttpResponse(response)