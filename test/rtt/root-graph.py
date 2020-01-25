#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt
import statistics
#import matplotlib.ticker as ticker


with open('./dataset/root1000.json') as f:
    _time = f.readline()
time = eval(_time)
time = [int(i) for i in time]

mean = statistics.mean(time)
median = statistics.median(time)
mode = statistics.mode(time)

x = list(range(1, 1001))

plt.grid(linestyle='-', linewidth=1)
plt.scatter(x, time, marker=".", color='darkorange', s=5)
plt.ylim([0, 500])
plt.xlabel('n-th(times)')
plt.xticks([])
plt.ylabel('Response Time(ms)')
plt.axhline(y=mean, color='royalblue', linestyle=':', label='Mean')
plt.axhline(y=median, color='royalblue', linestyle='--', label='Media')
plt.axhline(y=mode, color='royalblue', linestyle='-.', label='Mode')
plt.legend(bbox_to_anchor=(0.2, 0.95), loc='upper right', borderaxespad=0, fontsize=10)
plt.show()
