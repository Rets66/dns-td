#!/usr/bin/env python
# coding: utf-8

from twisted.internet import reactor
from twisted.names import dns, server



def main():
    factory = server.DNSServerFactory()
    protocol = dns.DNSDatagramProtocol(factory)

    reactor.listenUDP(10053, protocol)
    reactor.run()

if __name__ == '__main__':
    raise SystemExit(main())

