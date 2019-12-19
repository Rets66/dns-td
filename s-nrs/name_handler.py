#/usr/env python3
#encoding: utf-8

import socketserver #import DatagramRequestHandler, ThreadingUDPServer

from dnslib.dns import DNSHeader, DNSQuestion, DNSRecord, DNSError
from dnslib.buffer import Buffer, BufferError
from dnslib.label import DNSBuffer, DNSLabel
from redis import Redis


RCODE = {"NoError":0, "FormErr":1, "ServFail":2, "NXDomain":3}
QTYPE = {"A":1, "NS":2, "CNAME":5, "SOA":6, "PTR":12, "HINFO":13,
        "MX":15, "TXT":16, "RP":17, "AAAA":28, "HASHED":62}


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
        packet = DNSRecord.parse(data)
        packet_id , query_list = packet.header.id, str(packet.questions[0]).split()
        content_id, _rtype = query_list[0].strip(';'), query_list[-1]
        rtype = QTYPE[_rtype]
        value = Redis("127.0.0.1", 6379).get(content_id)

        # create response payload
        if value: # value = [obj, RR, Record Value, TTL]
            _ans, _ttl = value[-2], value[-1]
            response = DNSRecord(
                        DNSHeader(qr=1, aa=1, ra=1,
                        id=packet_id, rcode=RCODE["NoError"]))
            response.add_question(DNSQuestion(content_id, rtype))
            response.add_answer(RR(content_id, QTYPE.HASHED, rdata=_ans, ttl=_ttl))
        else:
            response = DNSRecord(
                        DNSHeader(qr=1, aa=1, ra=1,
                        id=packet_id, rcode=RCODE["NXDomain"]))
            response.add_question(DNSQuestion(content_id, rtype))
        payload = response.pack()
        connection.sendto(payload, self.client_address)


if __name__ == "__main__":
    addr = ("localhost", 10053)
    server = socketserver.UDPServer(addr, QueryHandler)
    with server:
        server.serve_forever()
