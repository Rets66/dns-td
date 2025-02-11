#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt
import statistics
#import matplotlib.ticker as ticker


with open('./calc_time5000.json') as f:
    data = f.readline()

time = eval(data)
time = [i * 1000 for i in time]
num = list(range(1,5001))

mean = statistics.mean(time)
median = statistics.median(time)
mode = statistics.mode(time)
#ave = sum(time) / 5000

plt.grid()
plt.scatter(num, time, marker=".", color='darkorange', s=1)
plt.ylim([0.0025, 0.004])
plt.xlabel('n-th(times)')
plt.ylabel('Calculation Time(ms)')
plt.axhline(y=mean, color='royalblue', linestyle=':', label='Mean')
plt.axhline(y=median, color='royalblue', linestyle='--', label='Media')
plt.axhline(y=mode, color='royalblue', linestyle='-.', label='Mode')
#plt.axhline(y=ave, xmin=0, xmax=5000, color='royalblue', label='Average')
plt.legend(bbox_to_anchor=(0.2, 0.95), loc='upper right', borderaxespad=0, fontsize=10)
#plt.legend(bbox_to_anchor=(1, 1.15), loc='upper right', borderaxespad=0, fontsize=10)
plt.show()
