#/usr/env python3
#encoding: utf-8

import socketserver #import DatagramRequestHandler, ThreadingUDPServer

from dnslib.dns import DNSHeader, DNSQuestion, DNSRecord
from dnslib.buffer import Buffer, BufferError
from dnslib.label import DNSBuffer, DNSLabel
from redis import Redis


RCODE = {"NoError":0, "FormErr":1, "ServFail":2, "NXDomain":3}


class QueryHandler(socketserver.BaseRequestHandler):
    """
    The DNS query handle server

    The suppoted query type is alread hashed, which's argment is qname and RR.
    Parsing the contentID(key), search in the Redis server.
    if it is able to find it, response the rcode and value.
    Otherwise, response only the rcode.
    """

    def handle(self):
        # handle query
        data, connection = self.request
        query = DNSRecord.parse(data).questions
        parser = str(query).split(' ')
        content_id = parser[2].strip("'")
        # create response payload
        q=DNSRecord(
                q=DNSQuestion(content_id)
                )
        try:
            ans, rcode, ttl = self.lookup(content_id)
            a=q.replyZone(
                    zone="{} {} IN {}".format(
                        content_id, ttl, ans))
            res = DNSRecord(header, q, a)
        except:
            rcode = RCODE["NXDomain"]
            header = DNSHeader(qr=1, aa=1, ra=1, rcode=rcode)
            res = DNSRecord(header, q)
        payload = DNSRecord.parse(res.pack())
        connection.sendto(payload, self.client_address)

    def lookup(self, key):
        self.conn = Redis("127.0.0.1", 6379)
        # value = [obj, RR, Record Value, TTL]
        value = self.conn.get(key)
        if value:
            ans, ttl = value[-2], value[-1]
            return ans, RCODE["NoError"], ttl
        else:
            return False
            #return "Not Match", , ttl


if __name__ == "__main__":
    addr = ("localhost", 10053)
    server = socketserver.UDPServer(addr, QueryHandler)
    with server:
        server.serve_forever()
