#!/usr/bin/env/ python3
#coding: utf-8

import random
import string
import json

#TLD = ['com', 'net', 'org', 'uk', 'info', 'de']
target_dist = 'exfil.com'


class DomainGenerater():
    def __init__(self):
        self.label_length = list(range(1, 64))
        self.label_number = list(range(2, 6))
        self.hostname_list= []

    def main(self, number):
        """Generate random domain name list"""
        for i in range(number):
            length = random.choice(self.label_length)
            hostname = self.gen_label(length)
            self.hostname_list.append(hostname)
        domain_name = [i + "." + target_dist for i in self.hostname_list]
        return domain_name

    def gen_label(self, length):
        """Generate random label"""
        characters = string.ascii_lowercase + string.digits
        selected_charalist = random.choices(characters, k=length)
        return "".join(selected_charalist)


if __name__ == '__main__':
    A = DomainGenerater()
    name_list = str(A.main(5000))
    with open("domain_list5000.json", "wt") as f:
        f.write(name_list)
