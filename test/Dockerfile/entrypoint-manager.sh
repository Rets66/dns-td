#!/bin/bash

pip3 install -r requirements-manager.txt 1>/dev/null
redis-server 1>/dev/null &
python3 manager.py &
exec "$@"
