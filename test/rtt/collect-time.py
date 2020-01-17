#!/usr/bin/env python3

import subprocess

with open('tlds-alpha-by-domain.txt') as f:
    data = f.readlines()
data = [i.strip('\n') for i in data]

def query(domain):
    proc = subprocess.run(['dig', '@100.10.1.3', domain], stdout=subprocess.PIPE)
    out = proc.stdout.decode('utf8')
    time = int(out.split(':\n')[-1].split('\n\n;;')[1].split('\n;;')[0].split(':')[1].strip(' ').strip('msec').strip(' '))
    return time

times = [query(i) for i in names]
target = dict(zip(names, times))
output = str(target)

with open('./rtt-time-test/test3.json', 'w') as f:
    f.write(output)
