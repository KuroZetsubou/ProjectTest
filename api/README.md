# API component (API, API_DB)

This folder contains the API service which listens to requests made by the web service, pushes the JSON on database and then sums the values in order to push them 

## Requirements

* Python 3.6+
* RabbitMQ server
* MongoDB

## How to run

It will run altogether with Docker configuration. However, if you want to run it standalone for debugging, you can use the following commands

```sh
python api/main.py # For running the HTTP server for API
python api/retreiveSatellitePush.py # For running the service which retreives from the broker the messages to update on MongoDB database
```

## Configuration

Open the `config.py` file 

* The following section is dedicated to MongoDB connection. However, Username/Password login is not supported yet, so make sure your (test) server supports the connection sans authentication for now.
```py
# PyMongo connection
MONGO_DATABASE = "project_test_api" # change this if you don't like it
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
```

* The following section is dedicated to HTTP server (using the `sanic` library). 

    If you want to expose it in a different host/port, make sure that you expose it on Docker (if you are going to use it on Docker) AND on `web/public/index.html` file on `line 7` as well.

```py
# Sanic configuration
SANIC_HOST = '0.0.0.0'
SANIC_PORT = 8083
SANIC_DEBUG = True
```

* The following section is dedicated to RabbitMQ configuration (credentials and queue names)

    Let's give a look at credentials:

```py
# RabbitMQ configuration

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

# please edit the credentials with yours
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"
```

> Those are default local connection to the broker. If necessary, edit the various parameters.

```py
# This declares the name of the queue for retreiving data from API service
RABBITMQ_QUEUE_NAME_PULL = "satellite_pull"
# This declares the name of the queue for pushing back the data to the API service
RABBITMQ_QUEUE_NAME_PUSH = "satellite_push"
```

> Now those above are the names of queues. The first one is for sending data from API service to the Satellite one; the second one vice versa.

> ⚠️ WARNING: If you are going to edit those values, edit them on `satellite/config.py` as well or the queue process will break!