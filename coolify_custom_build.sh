#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status.

echo "Building frontend with target..."
docker build \
  --target production-stage \
  -t perfumedia-frontend \
  -f ./frontend/production.Dockerfile \
  --build-arg VUE_APP_API_URL="${VUE_APP_API_URL}" \
  ./frontend

echo "Building other services..."
docker compose build postgres redis backend airflow-init airflow-webserver airflow-scheduler airflow-worker airflow-triggerer

echo "Custom build script finished."