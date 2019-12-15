#/usr/env python3
#encoding: utf-8

import os
import threading

from twisted.names import dns, server
from twisted.python import log


class NameQueryHandler:
    def __init__(self):
        self.factory = server.DNSServerFactory(
            clients=[client.Resolver(resolv='/etc/resolv.conf')]
        )
        self.protocol = dns.DNSDatagramProtocol(controller=self.factory)

    def serve(self, value):
        reactor.listenUDP(10053, self.protocol)
        reactor.listenTCP(10053, self.factory)
        reactor.run()

    def lookup(self, key):
        value = r.get(key)
        if value:
            return value
        else:
            raise pass # Error Record
