#!/usr/bin/env python3
# coding: utf-8

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

with open('range-map.json') as f:
    json_file = json.load(f)
    MADDR = [i['address'] for i in json_file]
    START_POINT = [i['range'][0] for i in json_file]

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
        data, connection = self.request
        packet = DNSRecord.parse(data)
        packet_id = packet.header.id
        name = str(packet.q.qname).rstrip('.')
        rtype_id = packet.q.qtype
        rtype = RTYPE[rtype_id]
        key = name + rtype
        sub_id = hashing(name.encode()).hexdigest()[:2]
        content_id = hashing(key.encode()).hexdigest()

        # find target manager
        pointer = bisect.bisect_left(START_POINT, content_id[:32]) - 1
        manager_addr = MADDR[pointer]

        # create transfer_packet
        header = DNSHeader(qr=0, aa=1, ra=1)
        transfer_packet = DNSRecord(header)
        transfer_packet.add_question(DNSQuestion(content_id))
        #response = transfer_packet.send(dst_ip)
        response = transfer_packet.send('100.10.1.4')
        d = DNSRecord.parse(response)
        # Create response packat
        header = DNSHeader(
                id=packet_id, qr=1, ra=1, aa=1, bitmap=d.header.rcode)
        ans_packet = DNSRecord(header)
        p = ans_packet.question(name)
        p = d.reply()

        if d.header.rcode == 0:  #NOERROR
            p.add_answer(RR.fromZone("{} {} {} {}".format(
                            name, d.a.ttl, QTYPE[rtype_id], str(d.a.rdata))
                        )
        else:pass
        connection.sendto(p, self.client_address)



if __name__ == '__main__':
    addr = ("0.0.0.0", PORT)
    server = socketserver.ThreadingUDPServer(addr, TransferHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
