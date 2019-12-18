#/usr/env python3
#encoding: utf-8

import io
import socketserver

from dnslib.server import DNSHandler
from dnslib.dns import DNSHeader, DNSQuestion, DNSRecord
from dnslib.buffer import Buffer, BufferError
from dnslib.label import DNSBuffer, DNSLabel
from redis import Redis


RCODE = {"NoError":0, "FormErr":1, "ServFail":2, "NXDomain":3}

class QueryHandler(DNSHandler):
    def __init__(self):
        self.rcode = 0
        self.conn = Redis("localhost", 6353)

    def lookup(self, key):
        value = self.conn.get(key)
        if value:
            self.rcode = 0
            return value, self.rcode
        else:
            self.rcode = 3
            return self.rcode

    def handle(self):
        """Need to handle whether query is hashed or not
        """
        data, connection = self.request
        msg = DNSRecord.parse(data).questions
        content_id = str(msg).split(' ')[2].strip("'")
        ans = self.lookup(content_id)
        packet = # id, response, rcode
        connnection.sendto(rdata, client_addr)


if __name__ == "__main__":
    addr = ("localhost", 10053)
    with socketserver.UDPServer(addr, QueryHandler) as server:
        server.serve_forever()
