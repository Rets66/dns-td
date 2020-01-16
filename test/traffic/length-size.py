#!/usr/bin/env python3
#coding: utf-8

import matplotlib.pyplot as plt

#length_list
length = list(range(11, 254))
#dns-td
dns_td_size = [145 for i in range(243)]

#dns
label_num1 = list(range(82, 325))
label_num2 = [i * 2 for i in label_num1]
label_num3 = [i * 3 for i in label_num1]
label_num4 = [i * 4 for i in label_num1]
label_num5 = [i * 5 for i in label_num1]


#plt.title('Relation between domain length and query packet size')
dns_td = plt.plot(length, dns_td_size, color='royalblue', label='DNS-TD')
dns_num1 = plt.plot(length, label_num1, color='darkorange', linestyle = ":", label='DNS Query Once')
dns_num2 = plt.plot(length, label_num2, color='darkorange', linestyle = "--", label='DNS Query Twice')
dns_num3 = plt.plot(length, label_num3, color='darkorange', linestyle = "-.", label='DNS Query Tree times')
dns_num4 = plt.plot(length, label_num4, color='darkorange', linestyle = "-", label='DNS Query four times')
#dns_num5 = plt.plot(length, label_num5, color='darkorange', linestyle = "dotted", label='DNS Query five times')

plt.grid()
plt.xlabel('Domain Length Size(bytes)')
plt.ylabel('Query Message Size(bytes)')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=1, fontsize=10)
plt.show()
