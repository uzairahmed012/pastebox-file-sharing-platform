#!/bin/bash
# Tear down the full stack and remove images if needed
set -e

echo "Stopping containers..."
docker-compose down

echo "Removing images (optional)..."
# docker rmi pastebox-server pastebox-client pastebox-selenium || true

echo "Cleanup complete."