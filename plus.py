from accessify import private, protected

class A:
     def t(self):
         _m1 = 0
         __m2 = 'qwrty'

a = A()
print (a.t._m1, a.t._A__m2)









