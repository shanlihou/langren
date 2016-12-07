from TestModel.models import Test
class DBHelper(object):
    @staticmethod
    def checkHas(name, date):
        try:
            test = Test.objects.get(name=name, date=date)
            if (test):
                return True
        except Test.DoesNotExist:
            return False
        return False
    
    @staticmethod
    def addUser(name, date):
        test1 = Test(date=date, name=name)
        test1.save()
    @staticmethod
    def getPpNum(date):
        userList = Test.objects.filter(date=date)
        return len(userList)