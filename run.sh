#!/bin/sh
rabbitmq-server -detached
sleep 2
screen -dm serve web/public -p 3000
sleep 2
screen -dm python3 api/main.py
sleep 2
screen -dm python3 satellite/main.py
sleep 2
screen -dm python3 api/retreiveSatellitePush.py
sleep 2
mongod --bind_ip 0.0.0.0
#screen -dmS webserver serve web/public -p 3000