# Web component (APP UI)

This folder contains the web interface which can be used to push the value(s) to the service API.

## Requirements

* Simple HTTP server (on Docker it simply runs `serve`)

## Configuration

The only thing to configure is at `line 7` of the `web/public/index.html` file the HTTP server of the API service in case of you are going to use a different host/port. Otherwise, keep it as default as provided