#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt
import statistics
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

mean = statistics.mean(ave_time)
median = statistics.median(ave_time)
mode = statistics.mode(ave_time)
print(mean, median, mode)

ave = sum(ave_time) / len(name)

#colorif = ['royalblue' if 20 > i else 'darkorange' for i in ave_time]
plt.grid(linestyle='-', linewidth=1)
#plt.figure(figsize=(10.0, 5.0))
plt.scatter(name, ave_time, marker=".", color='darkorange', s=10)
#plt.scatter(name, time1, marker=".", color='darkorange', s=10)
#plt.scatter(name, time2, marker=".", color='darkorange', s=10)
#plt.scatter(name, time3, marker=".", color='darkorange', s=10)
#plt.ylim([0, 500])
plt.xlabel('Top Level Domains(Three times average)')
plt.xticks([])
plt.ylabel('Response Time(ms)')
plt.axhline(y=mean, color='royalblue', linestyle=':', label='Mean')
plt.axhline(y=median, color='royalblue', linestyle='--', label='Media')
plt.axhline(y=mode, color='royalblue', linestyle='-.', label='Mode')
#plt.axhline(20, color='gray', linestyle='--', linewidth=1)
#plt.text(0, -10, '20')
#plt.axhline(y=ave, color='royalblue', label='Average')
plt.legend(bbox_to_anchor=(0.2, 0.95), loc='upper right', borderaxespad=0, fontsize=10)
#plt.legend(bbox_to_anchor=(1, 1.15), loc='upper right', borderaxespad=0, fontsize=10)
plt.show()
