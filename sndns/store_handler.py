#/usr/env python3
#encoding: utf-8

import socket
import socketserver

from redis import Redis


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
