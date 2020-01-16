#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker


with open('../../misc/dataset/hash-overhead/calc_time5000.json') as f:
    data = f.readline()

time = eval(data)
time = [i * 1000 for i in time]
num = list(range(1,5001))

ave = sum(time) / 5000

plt.grid()
plt.scatter(num, time, marker=".", color='darkorange', s=1, label='Calculation time')
plt.ylim([0.0025, 0.004])
plt.xlabel('n-th(times)')
plt.ylabel('Calculation Time(ms)')
plt.axhline(y=ave, xmin=0, xmax=5000, color='royalblue', label='Average')
plt.legend(bbox_to_anchor=(1, 1.15), loc='upper right', borderaxespad=0, fontsize=10)
plt.show()
