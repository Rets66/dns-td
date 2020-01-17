#!/usr/bin/env python3
#coding: utf-8

#import matplotlib.ticker as ticker

def ad(x, y, z):
    return (x + y + z) / 3

with open('./dataset/test1.json') as test1:
    _test1 = test1.readline()
test1 = eval(_test1)
with open('./dataset/test2.json') as test2:
    _test2 = test2.readline()
test2 = eval(_test2)
with open('./dataset/test3.json') as test3:
    _test3 = test3.readline()
test3 = eval(_test3)

name = [i for i in test1.keys()]
time1 = [int(i) for i in test1.values()]
time2 = [int(i) for i in test2.values()]
time3 = [int(i) for i in test3.values()]
ave_time = list(map(ad, time1, time2, time3))
target = str(dict(zip(name, ave_time)))

#target = {key:value for key, value in target.items() if value < 20}
with open('./dataset/average_rtt.json', 'w') as f:
    f.write(target)
