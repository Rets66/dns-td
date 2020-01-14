#!/usr/bin/env/ python3
#coding: utf-8

import random
import string
import json

TLD = ['com', 'net', 'org', 'uk', 'info', 'de']

class DomainGenerater():
    def __init__(self):
        self.label_length = list(range(1, 64))
        self.label_number = list(range(2, 6))
        self.domain_list = []

    def main(self, number):
        """Generate random domain name list"""
        hostname_list = []
        for i in range(number):
            length = random.choice(self.label_length)
            hostname = self.gen_label(length)
            hostname_list.append(hostname)
        for i in range(number):
            num = random.choice(self.label_number)
            candidate = random.choices(hostname_list, k=num)
            domain_name = self.gen_domain(candidate)
            self.domain_list.append(domain_name)
        return self.domain_list #["", "",..., ""]

    def gen_label(self, length):
        """Generate random domain label"""
        characters = string.ascii_lowercase + string.digits
        selected_charalist = random.choices(characters, k=length)
        return "".join(selected_charalist) # return like as '3h5iyrcp7jbj'

    def gen_domain(self, labels):
        """Generate domain name from random label"""
        tld = random.choice(TLD)
        labels.append(tld)
        return ".".join(labels)

if __name__ == '__main__':
    # intance
    A = DomainGenerater()
    name_list = str(A.main(10))
    with open("domain_list.json", "wt") as f:
        f.write(name_list)
