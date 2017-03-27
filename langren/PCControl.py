from TestModel.models import PC
class PCControl(object):
    def __init__(self):
        pass
    @staticmethod
    def setStatus(name, value):
        try:
            keyValue = PC.objects.get(name=name)
            if (keyValue):
                keyValue.value = value
                keyValue.save()
        except PC.DoesNotExist:
            keyValue = PC(name=name, value=value)
            keyValue.save()
    @classmethod
    def pcOpen(cls):
        cls.setStatus('pcStatus', 1)
        return 'success'
    @classmethod
    def pcClose(cls):
        cls.setStatus('pcStatus', 0)
        return 'success'
        
    @classmethod
    def wantOpen(cls):
        cls.setStatus('wantStatus', 1)
        return 'success'
    @classmethod
    def wantClose(cls):
        cls.setStatus('wantStatus', 0)
        return 'success'
        
    @staticmethod
    def getStatus(name):
        try:
            keyValue = PC.objects.get(name=name)
            if (keyValue):
                return keyValue.value
        except PC.DoesNotExist:
            return 0
    @classmethod
    def isNeedClose(cls):
        return cls.getStatus('wantStatus')
    @classmethod
    def isPCOpen(cls):
        return cls.getStatus('pcStatus')
        