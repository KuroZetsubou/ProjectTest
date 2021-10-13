#!/bin/sh
rabbitmq-server -detached
screen -dm serve web/public -p 3000
screen -dm python3 api/main.py
mongod
#screen python3 satellite/main.py