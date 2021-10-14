# Project Test

This is an entry test for Algorab.

## Requirements

* Windows, Linux (any distro should work fine) or macOS
* Docker

## How to run

### ⚠️ WARNING: Make sure that port 3000 and port 8083 are **NOT** used and your local MongoDB server is either using a different port or disabled

Run those two commands

```sh
docker build -t test .
docker run -p 3000:3000 -p 8083:8083 -p 27017:27017 test
```

Open on your browser the following link: http://localhost:3000/