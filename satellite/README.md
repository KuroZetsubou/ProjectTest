# Satellite component (SATELLITE, SATELLITE_DB)

This folder contains the satellite interface which receives via event commands the summed value to the database and then pushing it back to the API service (always via event command)

## Requirements

* Python 3.6+
* RabbitMQ server
* MongoDB

## How to run

It will run altogether with Docker configuration. However, if you want to run it standalone for debugging, you can use the following commands

```sh
python satellite/main.py # For running the Satellite service
```

## Configuration

Open the `config.py` file 

* The following section is dedicated to MongoDB connection. However, Username/Password login is not supported yet, so make sure your (test) server supports the connection sans authentication for now.
```py
# PyMongo connection
MONGO_DATABASE = "project_test_satellite" # change this if you don't like it
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
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

> ⚠️ WARNING: If you are going to edit those values, edit them on `api/config.py` as well or the queue process will break!