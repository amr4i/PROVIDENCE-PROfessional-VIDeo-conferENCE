#!/usr/bin/bash

gunicorn --threads 4 --workers 1 --bind 0.0.0.0:5000 app:app --certfile certificate.pem --keyfile key.pem --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker
