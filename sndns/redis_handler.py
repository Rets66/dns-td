#!/usr/bin/env python3
#encoding: utf-8

import redis
import subprocess
import sys

DB_HOST = 'localhost'
DB_PORT = 6353

class RedisHandler():
    def __init__(self):
        r = Redis(host=DB_HOST, port=DB_PORT)

    def log(self):
        log.startLogging(sys.stderr)

    def start(self):
        redis-server = ['/usr/local/bin/redis-server']
        start = subprocess.run(start_redis, capture_output=True)

    def store(self, key, value):
        r.set(key, value)

    def delete(self, key):pass

    def update(self, key):pass
