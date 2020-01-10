#/usr/env python3
#encoding: utf-8

import socketserver #import DatagramRequestHandler, ThreadingUDPServer
import threading

from dnslib.dns import *
from dnslib.buffer import Buffer, BufferError
from dnslib.bimap import Bimap,BimapError
from dnslib.label import DNSBuffer, DNSLabel
from redis import Redis


RCODE = {"NoError":0, "FormErr":1, "ServFail":2, "NXDomain":3}
QTYPE = {"A":1, "NS":2, "CNAME":5, "SOA":6, "PTR":12, "HINFO":13,
        "MX":15, "TXT":16, "RP":17, "AAAA":28, "HASHED":62}
RTYPE = {1:"A", 2:"NS", 5:"CNAME", 6:"SOA", 12:"PTR", 15:"MX",
        16:"TXT", 28:"AAAA", 62:"HASHED"}

# Redis needs to start befere the resolution starts
#def redis_handler():pass


class QueryHandler(socketserver.BaseRequestHandler):
    """
    The DNS query handle server

    The suppoted query type is already hashed, which's argment is qname and RR.
    Parsing the contentID(key), search in the Redis server.
    If it is able to find it, response the rcode and value.
    Otherwise, response only the rcode.
    """

    def handle(self):
        # handle query
        payload, connection = self.request
        p_id, c_id, qtype = self.parser(payload)
        b_value = self.resolute(c_id)
        if b_value:
            ttl, record = b_value[-2], b_value[-1]
            res = self.gen_packet(p_id, c_id, ttl, record)
        else:
            res = self.send_error(p_id, c_id)
        connection.sendto(res, self.client_address)

    def parser(self, payload):
        data = DNSRecord.parse(payload)
        p_id = data.header.id
        c_id = str(data.q.qname).strip('.')
        qtype = data.q.qtype
        return p_id, c_id, qtype

    def resolute(self, c_id):
        return Redis("127.0.0.1", 6379).get(c_id)

    def gen_packet(self, p_id, c_id, ttl, record):
        #ans, ttl = value[-2], value[-1]
        header = DNSHeader(qr=1, aa=1, ra=1,id=p_id, rcode=RCODE["NoError"]))
        res = DNSRecord(header)
        res.add_question(DNSQuestion(c_id, 'HASHED'))
        res.add_answer(*RR.fromZone("{} {} IN HASHED {}".format(content_id, ttl, record)))
        return response.pack()

        # if redis can't find the queried key, then the value sets 'None'
    def send_error(self, p_id, c_id):
        header = DNSHeader(qr=1, aa=1, ra=1,id=p_id, rcode=RCODE["NXDomain"]))
        res = DNSRecord(header)
        res.add_question(DNSQuestion(c_id, 'HASHED'))
        return res.pack()

if __name__ == "__main__":
    addr = ("0.0.0.0", 10053)
    server = socketserver.ThreadingUDPServer(addr, QueryHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
