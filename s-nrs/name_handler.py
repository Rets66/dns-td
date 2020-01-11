#/usr/env python3
#encoding: utf-8

import json
import socketserver
import subprocess
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
        data, connection = self.request
        query_data = self.parser(data)
        value = self.db_accesser(query_data['c_id'])

        # valeh
        if value: # value = [obj, RR, Record Value, TTL]
            ans = value.decode()
            ttl = '60'
            # answer = self.redis_parser(value)
            payload = self.gen_packet(
                    query_data['p_id'], query_data['c_id'],
                    query_data['q_type'], ttl, ans)
        else:
            payload = self.gen_error(
                    query_data['p_id'], query_data['c_id'], query_data['q_type'])
        payload = payload.pack()
        connection.sendto(payload, self.client_address)

    def parser(self, data):
        payload = DNSRecord.parse(data)
        p_id = payload.header.id
        c_id = str(payload.q.qname).rstrip('.')
        q_type = payload.q.qtype
        answer = {'p_id':p_id, 'c_id':c_id, 'q_type':q_type}
        return answer

    def db_accesser(self, c_id):
        return Redis("127.0.0.1", 6379).get(c_id)

    #def redis_parser(self, value):
    #   data = json.load(value.decode())
    #   answer = {'d_id':data[0], 'name':data[1], 'r_type':data[2],
    #               'ttl':data[3], 'rdata':data[4]}
    #   return answer

    # create response payload
    def gen_packet(self, p_id, c_id, q_type, ttl, record):
        payload = DNSRecord(
                    DNSHeader(qr=1, aa=1, ra=1,id=p_id, rcode=RCODE["NoError"]))
        payload.add_question(DNSQuestion(c_id, q_type))
        payload.add_answer(
                *RR.fromZone("{} {} A {}".format(c_id, ttl, record)))
        return payload


    def gen_error(self, p_id, c_id, q_type):
        payload = DNSRecord(DNSHeader(qr=1, aa=1, ra=1,
                    id=p_id, rcode=RCODE["NXDomain"]))
        payload.add_question(DNSQuestion(c_id, q_type))
        return payload


if __name__ == "__main__":
    addr = ("0.0.0.0", 10053)
    server = socketserver.ThreadingUDPServer(addr, QueryHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
