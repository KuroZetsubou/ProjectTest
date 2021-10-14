#!/usr/bin/env python

# Base source code: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika
import config
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.RABBITMQ_HOST, 
                                port=config.RABBITMQ_PORT, 
                                credentials=pika.PlainCredentials(
                                    username=config.RABBITMQ_USER, 
                                    password=config.RABBITMQ_PASS)
                            )
                        )
channel = connection.channel()

channel.queue_declare(queue=config.RABBITMQ_QUEUE_NAME_PULL)

test = {
    "idMessage": 999,
    "value": 999999
}

channel.basic_publish(exchange='', routing_key=config.RABBITMQ_QUEUE_NAME_PULL, body=json.dumps(test))
print(f" [x] Sent {test}")
connection.close()