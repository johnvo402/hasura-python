#!/bin/bash

# Add src directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Run the application
uvicorn webhook.main:app --reload --host 0.0.0.0 --port 8000