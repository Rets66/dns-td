#/usr/env python3
#encoding: utf-8

import socket
import json


content = json.dumps({"contentID" : "0c2b6ca6a823fc7d312e664448a88aba87a7456961035d060d5ff2e9c787f0bb","message" : {"object" : "www.example.com","rtype" : "A","Record Value" : "123.1.2.3","TTL" : 3800}})

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 9999))
    s.sendall(content.encode())
    data = s.recv(1024)
