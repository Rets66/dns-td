#/usr/env python3
#encoding: utf-8

import bisect
import csv
import hashlib
import json
import os
import socket
import socketserver

import sndns.redis_handler

SALT = ["repli", "repli2"]
PORT = 9999


class QueryHandler(socketserver.BaseRequestHandler):
    """
    The query handler class for nLm & another TLM.
    Both storing and Putting method are handled by this class.
    """
    def __init__(self):
        self.table = []
        with open('/etc/ddns/table.csv', newline='') as f:
            reader = csv.reader(f)
            for i in reader:
                self.table.append(i)

    def handle(self):
        data = self.request.recv(1024)
        payload = json.loads(data)
        method, ID, message = data['method'], data['contentID'], data['message']
        return method, ID, message
        #obj, rtype, ttl, record_value = message[0], payload[1], payload[2], payload[3:]

    def calc_key(self, obj, rtype, salt):
        query = [obj + rtype]
        queries += [obj + rtype + i for i in salt]
        bin_query = [bytes(i, encoding='utf-8') for i in queries]
        contentID = [hashlib.sha3_256(i).hexdigest() for i in bin_query]
        return contentID

    def find_dist(self, contentID):
        start = [i[0] for i in self.table]
        line = bisect.bisect_left(start, contentID) - 1
        #name, ip_addr = self.table[line][-1], self.table[line][-2]
        ip_addr = self.table[line][-2]
        return ip_addr

    def request(self, ip_addr, method, contentID, message):
        # TLM transfers the message & the method to the Area manager
        # dst = [start, end, address, manager name]
        content = json.dumps({"method":method, "contentID": contentID, "message":message})
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip_addr, PORT))
                s.sendall(content.encode())
            except:
                raise ConnectionError

    def store(self, dst):
        self.dst = dst
        DatabaseHandle().store(self.dst)
