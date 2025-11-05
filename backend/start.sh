#!/usr/bin/env bash
# start.sh

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app.main:app --host 0.0.0.0 --port 10000
