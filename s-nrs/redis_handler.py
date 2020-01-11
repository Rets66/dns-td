#!/usr/bin/env python3
#encoding: utf-8

from redis import Redis
import json
import sys

DB_HOST = 'localhost'
DB_PORT = 6353

class Server():
    def handler(self):
        data, connection = self.request
        query_data = self.parser(data)
        value = db_accesser(query_data['c_id'])
        if value:
            answer = self.redis_parser(value)
        else:
            self.res_nothing()

    def db_accesser(self, c_id):
        return Redis(host, port).get(c_id)

    def redis_parser(self, value):
        data = json.load(value)
        d_id = data[0]
        name = data[1]
        r_type = data[2]
        ttl = data[3]
        rdata = data[4]
        answer = {'d_id':d_id, 'name':name, 'r_type':r_type,
                'ttl':ttl, 'rdata':rdata}
        return answer



class RedisHandler():
    def __init__(self):
        r = Redis(host=DB_HOST, port=DB_PORT)

    def log(self):
        log.startLogging(sys.stderr)

    def start(self):
        redis-server = ['/usr/local/bin/redis-server']
        start = subprocess.run(redis-server, capture_output=True)

    def store(self, key, value):
        r.set(key, value)

    def delete(self, key):
        r.del(key)

    def update(self, key):pass

    def get_record(self, key):
        return r.get(key)
