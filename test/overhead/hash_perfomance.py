#!/usr/bin/env python3
#coding:utf-8

import time
from hashlib import sha3_224 as hashing

with open('domain_list5000.json') as f:
    line = f.readline()
domain_list = eval(line)

def calc(name, qtype):
    start_time = time.perf_counter()
    key = name + qtype
    d_id = hashing(name.encode()).hexdigest()[:28]
    c_id = hashing(key.encode()).hexdigest()
    end_time = time.perf_counter()
    calc_time = end_time - start_time
    return calc_time

if __name__ == "__main__":
    _time = [(i, "A") for i in domain_list]
    _ = str(_time)
    with open('calc_time5000.txt', 'w') as x:
        x.write(_)
