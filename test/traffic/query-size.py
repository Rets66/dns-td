#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt

## DNS-TD
dns_td_size = [145 for i in range(254)]

## DNS
overhead = 69
root = 1
length_position = 1
### Packet Size
root_p = root + overhead
tld = [(length_position + i + root + overhead) for i in range(2, 25)]
tld_p = [i *2 for i in tld]
base_line = [length_position + i + root + overhead for i in range(1, 254)]
label2 = [i * 2 for i in base_line]
label3 = [i * 3 for i in base_line]
label4 = [i * 4 for i in base_line]
label5 = [i * 5 for i in base_line]
print(label3[9:11])

## DNS Qname minimization
mini_tld = [(length_position + i + root + overhead) + root_p for i in range(2, 25)]

#plt.title('Relation between domain length and query packet size')
#query2root = plt.scatter(1, root_p, color='darkorange', linewidths='1', label='Query to Root')
dns_num5 = plt.plot(list(range(2, 255)), label5, color='darkorange', linestyle = ":", label='Forth Level Domain')
dns_num4 = plt.plot(list(range(2, 255)), label4, color='darkorange', linestyle = "-", label='Third Level Domain')
dns_num3 = plt.plot(list(range(2, 255)), label3, color='darkorange', linestyle = "-.",label='SLD')
query2tld = plt.plot(list(range(2, len(tld_p)+2)), tld_p, color='darkorange', linestyle = "--", label='TLD')
dns_td = plt.plot(list(range(len(dns_td_size))), dns_td_size, color='royalblue', label='DNS-TD')

plt.grid()
plt.xlabel('Domain Length Size(bytes)')
plt.ylabel('Total Query Packet Size(bytes)')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=1, fontsize=10)
plt.show()
