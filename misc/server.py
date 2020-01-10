#!/usr/bin/env python3
#coding: utf-8

import json
from hashlib import sha3_224 as hashing
import socketserver
import threading
import bisect

from dnslib.dns import DNSHeader, DNSQuestion, DNSRecord, DNSError
from dnslib.buffer import Buffer, BufferError
from dnslib.label import DNSBuffer, DNSLabel
#from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger

QTYPE = {"A":1, "NS":2, "CNAME":5, "SOA":6, "PTR":12,"MX":15,
        "TXT":16, "AAAA":28, "HASHED":62}
RTYPE = {1:"A", 2:"NS", 5:"CNAME", 6:"SOA", 12:"PTR", 15:"MX",
        16:"TXT", 28:"AAAA", 62:"HASHED"}
PORT = 19953

class TransferHandler(socketserver.BaseRequestHandler):
    """
    The request handler class like as Recursive Server.

    This handler deal with queries from stab resolver.
    The core methods are as follows:
     * create hashed Qname, then qtype is set "HASHED"
     * transfer the query to DHT manager based on Address Mapping Table
    """

    def handle(self):
        """The handle method from stab resolver"""
        payload, socket = self.request
        p_id, name, q_type, q_typeid = self.parser(payload)
        d_id, c_id = self.calc(name, q_type)
        m_addr = self.find(start_point, maddr, c_id)
        rcode, rdata = self.query(c_id, m_addr)
        answer = self.gen_packet(p_id, name, rcode, q_typeid, rdata)
        socket.sendto(answer.pack(), self.client_address)

    def parser(self, payload):
        data = DNSRecord.parse(payload)
        p_id = data.header.id
        name = str(data.q.qname).rstrip('.')
        q_typeid = data.q.qtype
        q_type = RTYPE[q_typeid]
        return p_id, name, q_type, q_typeid

    def find(self, start_addr, maddr, c_id):
        pointer = bisect.bisect_left(start_addr, c_id[:32]) - 1
        return maddr[pointer]

    def calc(self, name, qtype):
        key = name + qtype
        d_id = hashing(name.encode()).hexdigest()[:2]
        c_id = hashing(key.encode()).hexdigest()
        return d_id, c_id

    def query(self, c_id, m_addr):
        header = DNSHeader(qr=0, aa=1, ra=1)
        transfer_packet = DNSRecord(header)
        transfer_packet.add_question(DNSQuestion(c_id))
        response = transfer_packet.send(dest=m_addr, port=10053)
        ans = DNSRecord.parse(response)
        rcode, rdata = ans.header.rcode, str(ans.a.rdata)
        return rcode, rdata

    def gen_packet(self, p_id, qname, rcode, q_typeid, rdata):
        header = DNSHeader(id=p_id, qr=1, ra=1, aa=1, bitmap=rcode)
        packet = DNSRecord(header)
        packet.add_question(DNSQuestion(qname))
        if rcode == 0:  #NOERROR
            packet.add_answer(RR.fromZone("{} {} {} {}".format(name, answer_data.a.ttl, q_typeid, str(rdata))))
            return packet
        else:
            return packet


if __name__ == '__main__':
    with open('range-map.json') as f:
        json_file = json.load(f)
        maddr = [i['address'] for i in json_file]
        start_point = [i['range'][0] for i in json_file]

    addr = ("0.0.0.0", PORT)
    server = socketserver.ThreadingUDPServer(addr, TransferHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
