#!/bin/bash
# Bring up the full stack via docker-compose
set -e

echo "Bringing down existing stack (if any)..."
docker-compose down || true

echo "Starting services..."
docker-compose up -d --build

echo "Waiting for services to stabilize..."
sleep 10

echo "Services started:"
docker-compose ps

echo "To follow logs: docker-compose logs -f"