from __future__ import unicode_literals

from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=40)
    date = models.CharField(max_length=10)
    
class Identy(models.Model):
    name = models.CharField(max_length=40)
    number = models.IntegerField()
    status = models.IntegerField()
    identy = models.CharField(max_length=20)

class Status(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField()