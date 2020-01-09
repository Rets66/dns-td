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
RTYPE = {1:"A", 2:"NS", 5:"CNAME", 6:"SOA", 12:"PTR", 15:"MX",
        16:"TXT", 28:"AAAA", 62:"HASHED"}


class QueryHandler(socketserver.BaseRequestHandler):
    """
    The DNS query handle server

    The suppoted query type is already hashed, which's argment is qname and RR.
    Parsing the contentID(key), search in the Redis server.
    if it is able to find it, response the rcode and value.
    Otherwise, response only the rcode.
    """

    def handle(self):

        # handle query
        data, connection = self.request
        packet = DNSRecord.parse(data)
        packet_id = packet.header.id
        content_id = str(packet.q.qname)
        rtype = RTYPE[packet.q.qtype]
        value = Redis("127.0.0.1", 6379).get(content_id)

        # create response payload
        if value: # value = [obj, RR, Record Value, TTL]
            ans, ttl = value[-2], value[-1]
            response = DNSRecord(
                        DNSHeader(qr=1, aa=1, ra=1,
                        id=packet_id, rcode=RCODE["NoError"]))
            response.add_question(DNSQuestion(content_id, rtype))
            response.add_answer(
                    RR.fromZone("{} {} {} {}".format(
                        content_id, ttl, QTYPE.HASHED, ans))
                    )
        else:
            response = DNSRecord(
                        DNSHeader(qr=1, aa=1, ra=1,
                        id=packet_id, rcode=RCODE["NXDomain"]))
            response.add_question(DNSQuestion(content_id, rtype))
        payload = response.pack()
        connection.sendto(payload, self.client_address)


if __name__ == "__main__":
    addr = ("0.0.0.0", 10053)
    server = socketserver.ThreadingUDPServer(addr, QueryHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever())
