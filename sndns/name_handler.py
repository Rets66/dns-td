#/usr/env python3
#encoding: utf-8

import csv
import hashlib
import os
import socket
import socketserver
import sys
import threading

from twisted.names import dns, server
from twisted.python import log


class NameQueryHandler:
    def __init__(self):
        self.factory = server.DNSServerFactory(
            clients=[client.Resolver(resolv='/etc/resolv.conf')]
        )
        self.protocol = dns.DNSDatagramProtocol(controller=self.factory)

    def log(self):
        log.startLogging(sys.stderr)

    def serve(self):
        reactor.listenUDP(10053, self.protocol)
        reactor.listenTCP(10053, self.factory)
        reactor.run()

    def lookup(self, key):
        r = Redis(host=DB_ADDR[0], port=DB_ADDR[1])
        value = r.get(key)
        if value:
            return value
        else:
            raise pass # Error Record

    def response(self, value):pass
