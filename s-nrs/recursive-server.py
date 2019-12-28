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
        # Required: packet id, src, dst, payload, rtype
        data, connection = self.request
        packet = DNSRecord.parse(data)
        packet_id = packet.header.id
        name = str(packet.q.qname).rstrip('.')
        _rtype = packet.q.qtype
        rtype = RTYPE[_rtype]
        key = name + rtype
        sub_id = hashing(name.encode()).hexdigest()[:2]
        content_id = hashing(key.encode()).hexdigest()

        # find target manager
        pointer = bisect.bisect_left(START_POINT, content_id[:32]) - 1
        manager_addr = MADDR[pointer]

        # create transfer_packet
        header = DNSHeader(qr=1, aa=1, ra=1)
        transfer_packet = DNSRecord(header)
        transfer_packet.add_question(DNSQuestion(content_id))
        transfer_packet = transfer_packet.pack()
        # transfer
        ans = payload_manager.send(dst_ip)


        # response
#        r_packet = DNSRecord(ans)
#
#        _id, ans_rcode, ans_obj, _rtype, ans_body = parse_dpacket(response)
#        answer = create_packet(
#                    query-response=1, packet_id=query_id
#                    rcode=ans_rcode, name=obj, recode_type=query_rtype)
#        if ans_rcode == 0:  #NOERROR
#            answer.add_answer(RR(res_obj, query_rtype,rdata=query_rtype, ttl=ttl))
#        else:pass
#        client_addr = (dst, port)
#        connection.sendto(answer, self.client_addr)

    def create_packet(self, query_response, packet_id, status, name, recode_type):
        return packet

if __name__ == '__main__':

    addr = ("localhost", PORT)
    server = socketserver.ThreadingUDPServer(addr, TransferHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
#    resolver = TransferHandler()
#    udp_server = DNSServer(resolver,port=PORT, address='localhost')
#    udp_server.start_thread()
