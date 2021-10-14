# base imports
import pika
import json as _json
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

# Sanic import
import sanic
from sanic.response import json, file_stream, file, text
from aiofiles import os as async_os

# config import
import config

# Lib import
from lib.mongo import MongoConnection, MongoConnectionConfig

# MongoDB connection
db = MongoConnection(MongoConnectionConfig)
# RabbitMQ connection
# Base source code: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
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

async def test(request):
    return json({"hello": "world"})

async def pushData(request: sanic.Request):
    
    # JSON check
    try:
        req = request.json
        print(req)
    except:
        return text("not a json", 400)

    if req is None:
        return text("empty body", 400)

    # saving data
    _savedId = db.addMessage(_json.dumps(req))

    bodyForSatellite = {"idMessage": _savedId, "value": 0}

    for entry in req:
        bodyForSatellite["value"] += entry["value"]

    print(bodyForSatellite)
    channel.basic_publish(exchange='', routing_key=config.RABBITMQ_QUEUE_NAME_PULL, body=_json.dumps(bodyForSatellite))

    # return ok status
    return text("ok")

# Exported routes for the server
def add_external_routes(app):
    # GET
    app.add_route(test, '/', methods=["GET"])
    

    # POST
    app.add_route(pushData, '/api/push', methods=['POST'])

    @app.middleware('response')
    async def print_on_response(request, response: sanic.response.BaseHTTPResponse):
        print("I print when a response is returned by the server")
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "GET, POST"

    @app.middleware('request')
    async def prerequest(request: sanic.request.Request):
        print("request made:", request.headers)