#!/usr/bin/env bash
<<<<<<< HEAD
# start.sh

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
=======
set -e
cd frontend
npm install --silent
npm run build --silent
cd ..
pip install -r backend/requirements.txt
cd backend
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de
uvicorn app.main:app --host 0.0.0.0 --port 10000
