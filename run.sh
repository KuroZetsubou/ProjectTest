#!/bin/sh
rabbitmq-server -detached
screen -dm -xS webserver serve web/public -p 3000
screen -dm -xS apiserver python3 api/main.py
screen -dm -xS apiserver_broker python3 api/retreiveSatellitePush.py
screen -dm -xS satellite python3 satellite/main.py
mongod --bind_ip 0.0.0.0