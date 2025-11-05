#!/usr/bin/env bash
set -e
cd frontend
npm install --silent
npm run build --silent
cd ..
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 10000
