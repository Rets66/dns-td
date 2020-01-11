#!/bin/bash

pip3 install -r requirements-resolver.txt
python3 full-resolver.py
exec "$@"
