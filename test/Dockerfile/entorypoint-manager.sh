#!/bin/bash

pip3 install -r requirements-manager.txt
python3 manager.py
exec "$@"
