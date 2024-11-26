#!/bin/bash

echo "Starting REST API Service..."
python3 services/rest_api_service.py &

echo "Starting Filter Service..."
python3 services/filter_service.py &

echo "Starting SCREAMING Service..."
python3 services/screaming_service.py &

echo "Starting Publish Service..."
python3 services/publish_service.py &

wait
