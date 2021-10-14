# PyMongo connection
MONGO_DATABASE = "project_test_api" # change this if you don't like it
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''

# Sanic configuration
SANIC_HOST = '0.0.0.0'
SANIC_PORT = 8083
SANIC_DEBUG = True

# RabbitMQ configuration

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
# please edit the credentials with yours
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"
# This declares the name of the queue for retreiving data from API service
RABBITMQ_QUEUE_NAME_PULL = "satellite_pull"
# This declares the name of the queue for pushing back the data to the API service
RABBITMQ_QUEUE_NAME_PUSH = "satellite_push"