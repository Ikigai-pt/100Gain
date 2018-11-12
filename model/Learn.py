class Learn:
    accessPublic = 'public attribute'
    __accessPrivate = 'private attribute'
    _accessProtected = 'protected attribute'

    def __init__(self, name):
        print ( "init called" )
        self.accessPublic = name

    def getPrivateVariable(self):
        return self.__accessPrivate


l = Learn("test");
print(l.getPrivateVariable())
print(l.accessPublic)
print(Learn.accessPublic)
l.accessPublic = 'changed'
print(Learn.accessPublic)
print(l.accessPublic)
n = Learn("newTest");
n.accessPublic

