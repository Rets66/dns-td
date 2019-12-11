#/usr/env python3
#encoding: utf-8

import bisect
import csv
import hashlib
import os
import socket
import socketserver

from redis import Redis

SALT = ["repli", "repli2"]
DB_ADDR = {"addr" : "localhost", "port" : xxx}

class StoreHandler(socketserver.BaseRequestHandler):
    def __init__(self):
        DatabaseHandler().start()

    def handle(self, value):
        data = self.request.recv(1024)
        value = data[].split(',')
        name, rtype, record_value = value[0], value[1], value[2:]

    def store(self, dst):
        self.dst = dst
        DatabaseHandle().store(self.dst)

class DatabaseHandler:
    def start(self):pass

    def store(self, key, value):
        r = Redis(host='', port='')
        r.set(key, value)

    def delete(self, key):pass

STORE_PORT = 8080


class PutHandler(socketserver.BaseRequestHandler):
    def __init__(self, content, table):
        self.content = content
        self.table = []
        with open('/etc/ddns/table.csv', newline='') as f:
            reader = csv.reader(f)
            for i in reader:
                self.table.append(i)

    def handle(self): # server
        data = self.request.recv(1024)
        value = data[]

    def calc_key(self, name, rtype, salt):
        query = [name + rtype]
        queries += [name + rtype + i for i in salt]
        bin_query = [bytes(i, encoding='utf-8') for i in queries]
        content_id = [hashlib.sha3_256(i).hexdigest() for i in bin_query]
        return content_id

    def find_manager(self, target):
        start = [i[0] for i in self.table]
        index = bisect.bisect_left(start, target)
        manager = self.table[index]
        return manager

    def request(self, dst, content):
        addr = (dst[2], STORE_PORT)     # dst = [start, end, address, name]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(addr)
            s.sendall(content.encode())
