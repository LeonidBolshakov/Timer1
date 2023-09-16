from accessify import private, protected
from math import sqrt
import pytest

class Point:

#    @protected
    def check_coord(self, coord):
        if not type( coord ) in (int, float):
            raise Exception( f'The {coord} coordinate is not a number.' )
        else:
            return coord

    def __init__(self, x, y):

        self.__x = self.check_coord(x)
        self.__y = self.check_coord(y)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
       self.__x = self.check_coord(x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
       self.__y = self.check_coord(y)

    def __str__(self):
        return f'{self.__x = }, {self.__y = }'

def dist_point(p1: Point, p2: Point) -> float:
    return sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

p1 = Point(3.2, -3)
p2 = Point(0,4)

pytest.raises(Exception, Point, "3", 1)
pytest.raises(Exception, Point, 3, "1")
assert dist_point(Point(3.2, -3), Point(0,4)) == 7.696752561957543
p1 = Point(0, 1)
p1.x = 3
p1.y = 4
assert str(p1) == 'self.__x = 3, self.__y = 4'

import time

#for i in range(11):
#    time.sleep(1)
#    print(time.time(), datetime.datetime.now())

class MySleep:
    def __init__(self, sec):
        self.__zero_time__ = time.time()
        self.sec = sec

    def end_request(self, stage):
        return time.time() <= self.__zero_time__ + self.sec * stage

my_sleep = MySleep(sec=1)
for i in range(11):
    while(my_sleep.end_request(stage=i+1)):
        time.sleep(0.001)
    print(time.time())











