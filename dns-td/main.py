#/usr/env python3
#encoding: utf-8

import socketserver

import sndns.dht_hanler

if __name__ == '__main__':
    os.mkdir('/etc/ddns')
    with socketserver.TCPServer((HOST, PORT), QueryHandler):
        server.serve_forever()
