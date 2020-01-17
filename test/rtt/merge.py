#!/usr/bin/env python3
#coding: utf-8


with open('time_list.json') as f:
    _time = f.readline()
time = eval(_time)
time = [int(i) for i in time]

with open('tlds-alpha-by-domain.txt') as f:
    _name = f.readlines()

name = [i.strip(',\n') for i in _name]

target = dict(zip(name, time))
target = str(target)

with open('tlds_rtt.json', 'w') as f:
    f.write(target)

# {'name' :['com'],
#  'time' : [1]}
