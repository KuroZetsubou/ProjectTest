#!/bin/sh
echo "RabbitMQ Server start"
rabbitmq-server -detached
echo "Web Server"
sleep 2
screen -dm serve web/public -p 3000
echo "API Server"
sleep 2
screen -dm python3 api/main.py
echo "Satellite Server"
sleep 2
screen -dm python3 satellite/main.py
echo "API RabbitMQ Receiver Service"
sleep 2
screen -dm python3 api/retreiveSatellitePush.py
echo "MongoDB"
sleep 2
mongod --bind_ip 0.0.0.0