#!/usr/bin/env python
import pika, sys, os
import json
import config
from lib.mongo import MongoConnectionConfig, MongoConnection

def main():

    db = MongoConnection(config=MongoConnectionConfig)

    parameters = pika.ConnectionParameters()
    parameters.host = config.RABBITMQ_HOST
    parameters.port = config.RABBITMQ_PORT
    parameters.credentials = pika.PlainCredentials(
        username=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASS
    )

    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=config.RABBITMQ_QUEUE_NAME_PUSH)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

        try:
            data = json.loads(body)
        except json.decoder.JSONDecodeError:
            return

        if data is None:
            return

        db.updateMessage(id=data['idMessage'], idReference=data['idReference'], referenceDateTime=data['referenceDateTime'])

    channel.basic_consume(queue=config.RABBITMQ_QUEUE_NAME_PUSH, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        print("connection...")
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)