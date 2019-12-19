#!/usr/bin/env python3
# coding: utf-8

import csv
import hashlib
import socketserver
import threading

from dnslib.dns import DNSHeader, DNSQuestion, DNSRecord, DNSError
from dnslib.buffer import Buffer, BufferError
from dnslib.label import DNSBuffer, DNSLabel

QTYPE = {"A":1, "NS":2, "CNAME":5, "SOA":6, "PTR":12, "HINFO":13,
        "MX":15, "TXT":16, "RP":17, "AAAA":28, "HASHED":62}
PORT = 19953


class TransferHandler(socketserver.BaseRequestHandler):
    """
    The request handler class like as Recursive Server.

    This handler deal with queries from stab resolver.
    The core methods are as follows:
     * create hashed Qname, then qtype is set "HASHED"
     * transfer the query to DHT manager based on Address Mapping Table
    """

    def __init__(self):
        self.table = []
        with open('/Users/shoretsu-t/git/range-map.csv', newline='') as f:
            reader = csv.reader(f)
            for i in reader:
                self.table.append(i)

    def find_dst(self, contentID):
        start = [i[0] for i in self.table]
        line = bisect.bisect_left(start, contentID) - 1
        #name, ip_addr = self.table[line][-1], self.table[line][-2]
        dst_ipaddr = self.table[line][-2]
        return dst_ipaddr

    def parse_dpacket(self, packet):
        data = DNSRecord.parse(packet)
        id, rcode = packet.header.id, packet.header.rcode
        query_list = str(packet.questions[0]).split()
        obj, rtype = query_list[0].strip(';'), query_list[-1]
        return id, rcode, obj, rtype, data

    def create_packet(self, query-response, packet_id, status, name, recode_type):
        packet = DNSRecord(
                    DNSHeader(qr=query-response, aa=1, ra=1,
                    id=packet_id, rcode=status))
        packet.add_question(name, recode_type)
        return packet

    def handle(self):
        # Required: packet id, src, dst, payload, rtype
        data, connection = self.request
        packet = DNSRecord.parse(data)
        query_id, status, obj, query_rtype, query_body = parse_dpacket(packet)
        content = obj + query_rtype
        content_id = hashlib.sha3_256(content.encode()).hexdigest()
        # find target manager
        dst_ip = find(content_id)
        # create packet
        init_packet_manager = create_packet(
                query-response=0, packet_id=id,
                rcode=status, name=obj,
                recode_type=QTYPE["HASHED"])
        payload_manager = init_payload_manager.pack()
        # transfer
        response = payload_manager.send(dst_ip)
        # response
        _id, ans_rcode, ans_obj, _rtype, ans_body = parse_dpacket(response)
        answer = create_packet(
                    query-response=1, packet_id=query_id
                    rcode=ans_rcode, name=obj, recode_type=query_rtype)
        if ans_rcode == 0:  #NOERROR
            answer.add_answer(RR(res_obj, query_rtype,rdata=query_rtype, ttl=ttl))
        else:pass
        client_addr = (dst, port)
        connection.sendto(answer, self.client_addr)


if __name__ == '__main__':
    addr = ("localhost", PORT)

    server = socketserver.ThreadingUDPServer(addr, TransferHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
