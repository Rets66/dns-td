#!/usr/bin/env/ python3
#coding: utf-8

import random
import string

def gen_label(length):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def main():
    label_length = random.choice(range(1,64))
    label = gen_label(label_length)
    domain = ".".join(label)
