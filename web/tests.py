import time

from django.test import TestCase

# Create your tests here.
def loop_func(func, second, end):
    tes = "aaa"
    teee = [1223]
    ttt = object()
    start_time1 = 2313213
    def inner():

        while start_time1 < end +1:
            print(start_time1)
            func()
            print(tes)
            print(teee)
            print(ttt)
            try:
                print("输出start_time1: ", start_time1)
            except Exception as e:
                print(e)
            time.sleep(second)
            start_time1 = start_time1 + second
    return inner
def ddd():
    print(1)
g = loop_func(ddd, 1, 5)
g()