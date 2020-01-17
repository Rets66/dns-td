#!/usr/bin/env python3

import subprocess

def query():
    proc = subprocess.run(['dig', '@100.10.1.3', '.'], stdout=subprocess.PIPE)
    out = proc.stdout.decode('utf8')
    time = int(out.split(':\n')[-1].split('\n\n;;')[1].split('\n;;')[0].split(':')[1].strip(' ').strip('msec').strip(' '))
    subprocess.run(['unbound-control', 'reload'])
    return time


times = [query() for i in range(100)]
print(times)

#with open('./rtt-time-test/test3.json', 'w') as f:
#    f.write(output)
