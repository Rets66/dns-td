#!/usr/bin/env python3
# coding: utf-8

import socket

addr = ("localhost", 19953)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"yahoo.com", addr)
