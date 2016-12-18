#!/usr/bin/python
#coding:utf-8
from TestModel.models import Status,Identy
import string
class GAME(object):
    userIdenty = ['wolf', 'hunt', 'seer', 'witch', 'cupid', 'guard', 'idiot', 'white_wolf', 'thief']
    badIdenty = ['wolf', 'idiot', 'white_wolf']
    @staticmethod
    def reset():
        Identy.objects.all().delete()
        Status.objects.all().delete()
        opt = Status(name='night', value=0)
        opt.save()
        opt = Status(name='save', value=0)
        opt.save()
        opt = Status(name='poison', value=0)
        opt.save()
    @staticmethod
    def get(name):
        try:
            user = Identy.objects.get(name=name)
            if (user):
                return user
        except Identy.DoesNotExist:
            return None
    @staticmethod
    def getDeadLink(num):
        link = Identy.objects.filter(status=3)
        retList = []
        for var in link:
            retList.append(var.number)
        if num in retList:
            return retList
        else:
            return [num]
    @staticmethod
    def killNum(num):
        user = Identy.objects.get(number=num)
        user.status -= 1
        user.save()
    @staticmethod
    def isDead(num):
        user = Identy.objects.get(number=num)
        if user.status & 1:
            return True
        return False    
    @classmethod
    def getDead(cls):
        kill = cls.getStatus('kill')
        save = cls.getStatus('save')
        night = cls.getStatus('night')
        guard = cls.getStatus('guard')
        deadList = None
        retStr = ''
        if save == night:
            if kill == guard:
                deadList = cls.getDeadLink(kill)
        else:
            if kill != guard:
                deadList = cls.getDeadLink(kill)
        poison = cls.getStatus('poison')
        if poison:
            if not cls.isDead(poison):
                if poison not in deadList:
                    deadList += cls.getDeadLink(poison)
        for i in deadList:
            cls.killNum(i)
            retStr += str(i) + ' '
        return retStr
    @classmethod
    def enter(cls, status):
        old = cls.getStatus('status')
        try:
            keyValue = Status.objects.get(name='status')
            if (keyValue):
                keyValue.value = status
                keyValue.save()
        except Status.DoesNotExist:
            keyValue = Status(name='status', value=status)
            keyValue.save()
        if old != status and status == 2:
            opt = Status.objects.get(name='night')
            opt.value = opt.value + 1
            opt.save()
        elif status == 3:
            return cls.getDead()
        return None
    @staticmethod
    def getStatus(name):
        try:
            keyValue = Status.objects.get(name=name)
            if (keyValue):
                return keyValue.value
        except Status.DoesNotExist:
            return 0
    @classmethod
    def getKill(cls, name):
        if not cls.isIdenty(name, 'witch'):
            print 'not witch'
            return 0
        return cls.getStatus('kill')
        
    @staticmethod
    def getLink():
        link = Identy.objects.filter(status=3)
        retStr = ''
        for var in link:
            retStr += str(var.number) + ' '
        return retStr
    @classmethod
    def getMine(cls, name):
        mine = cls.get(name)
        strRet = ''
        if (mine):
            strRet = '身份:' + mine.identy + '\n'
            strRet += '编号:' + str(mine.number) + '\n'
            strRet += '是否健在:'
            if mine.status & 1:
                strRet += '在世\n'
            else:
                strRet += '去世\n'
            strRet += '配偶:'
            if mine.status & 2:
                strRet += cls.getLink() + '\n'
            else:
                strRet += '别想了，单身狗\n'
        else:
            return '你不存在'
        return strRet
    @staticmethod
    def getLive():
        userList = Identy.objects.all()
        retStr = ''
        for var in userList:
            if var.status & 1:
                retStr += str(var.number) + ' '
        return retStr
    @classmethod
    def save(cls, name):
        if (cls.getStatus('status') != 2):
            return False
        if not cls.isIdenty(name, 'witch'):
            return False
        if cls.getStatus('save') != 0:
            return False
        day = cls.getStatus('night')
        opt = Status.objects.get(name='save')
        opt.value = day 
        opt.save()
        return True
    @classmethod
    def shoot(cls, name, number):
        if (cls.getStatus('status') != 3):
            return '操作失败'
        if not cls.isIdenty(name, 'hunt'):
            return '操作失败'
        user = Identy.objects.get(name=name)
        if user.number == cls.getStatus('poison'):
            return '操作失败'
        cls.killNum(string.atoi(number))
        return '操作成功'
    @classmethod
    def poison(cls, name, number):
        if (cls.getStatus('status') != 2):
            return False
        if not cls.isIdenty(name, 'witch'):
            return False
        opt = Status.objects.get(name='poison')
        if opt.value != 0:
            return False
        opt.value = string.atoi(number)
        opt.save()
        return True
    @classmethod
    def getWolf(cls, name, number):
        if (cls.getStatus('status') != 2):
            return '操作失败'
        if not cls.isIdenty(name, 'seer'):
            return '操作失败'
        user = Identy.objects.get(number=string.atoi(number))
        if user.identy in cls.badIdenty:
            return '他是坏人'
        return '他是好人'
    @classmethod
    def guard(cls, name, number):
        if (cls.getStatus('status') != 2):
            return '操作失败'
        if not cls.isIdenty(name, 'guard'):
            return '操作失败'
        num = string.atoi(number)
        try:
            opt = Status.objects.get(name='guard')
            opt.value = num
            opt.save()
        except Status.DoesNotExist:
            opt = Status(name='guard', value=num)
            opt.save()
        return '操作成功'
        
    @staticmethod
    def getAllUser():
        userList = Identy.objects.all()
        strRet = '人数:' + str(len(userList)) + '人\n'
        if len(userList) == 0:
            return strRet
        strRet += '分别是:'
        for var in userList:
            strRet += str(var.number) + ' '
        return strRet
    @staticmethod
    def isIdenty(name, identy):
        try:
            user = Identy.objects.get(name=name, identy=identy)
            if (user):
                return True
        except Identy.DoesNotExist:
            return False
    @classmethod
    def kill(cls, name, number):
        if (cls.getStatus('status') != 2):
            return False
        if not cls.isIdenty(name, 'wolf'):
            return False
        num = string.atoi(number)
        try:
            opt = Status.objects.get(name='kill')
            opt.value = num
            opt.save()
        except Status.DoesNotExist:
            opt = Status(name='kill', value=num)
            opt.save()
        return True
    @classmethod
    def link(cls, name, str1, str2):
        if (cls.getStatus('status') != 2):
            return False
        if not cls.isIdenty(name, 'cupid'):
            return False
        linkUser = Identy.objects.filter(status=3)
        for var in linkUser:
            var.status = 1
            var.save()
            
        num1 = string.atoi(str1)
        num2 = string.atoi(str2)
        user1 = Identy.objects.get(number=num1)
        user2 = Identy.objects.get(number=num2)
        user1.status = 3
        user1.save()
        user2.status = 3
        user2.save()
        return True
    @classmethod
    def add(cls, name, number, identy):
        if identy not in cls.userIdenty:
            print (identy)
            return False
        if (cls.getStatus('status') != 1):
            print 'status false'
            return False
        user = cls.get(name)
        if (user):
            user.number = number
            user.identy = identy
            user.status = 1
        else:
            user = Identy(name=name, number=number, identy=identy, status=1)
        user.save()
        return True