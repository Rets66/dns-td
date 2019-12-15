#/usr/env python3
#encoding: utf-8

import socketserver
import json

class QueryHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        payload = json.loads(data)
        contentID = payload['contentID']
        message = payload['message']
        print(contentID)
        print(message)


if __name__ == '__main__':
    with socketserver.TCPServer(('localhost', 9999), QueryHandler) as server:
        server.serve_forever()
