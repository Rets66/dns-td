#!/usr/bin/env/ python3
#coding: utf-8

import random
import string
import json

#TLD = ['com', 'net', 'org', 'uk', 'info', 'de']
target_dist = 'exfil.com'


class DomainGenerater():
    def __init__(self):
        self.domain_length = list(range(1, 64))
        self.hostname_list= []

    def main(self, number):
        """Generate domain name from 1 digits to 253 digits"""
        labels = [self.gen_label(i) for i in self.domain_length]
        domain_name = [i + "." + target_dist for i in labels]
        forth = [i + "." + self.gen_label(63) + "." + target_dist for i in  labels]
        domain_name.extend(forth)
        fifth = [i + "." + self.gen_label(63) + "." + self.gen_label(63) + "." + target_dist for i in  labels]
        domain_name.extend(fifth)
        sixth = [i + "." + self.gen_label(63) + "." + self.gen_label(63) + "." + self.gen_label(63) + "." + target_dist for i in  labels]
        domain_name.extend(sixth)
        return domain_name

    def gen_label(self, length):
        """Generate label based on length"""
        characters = string.ascii_lowercase + string.digits
        selected_charalist = random.choices(characters, k=length)
        return "".join(selected_charalist)


if __name__ == '__main__':
    A = DomainGenerater()
    name_list = str(A.main(100))
    with open("domain_list_for_estimate_size.json", "wt") as f:
        f.write(name_list)
