#!/bin/bash
# Build all Docker images for PasteBox
set -e

echo "Building server image..."
docker build -t pastebox-server:latest ./server

echo "Building client image..."
docker build -t pastebox-client:latest ./client

echo "Building selenium test image..."
docker build -t pastebox-selenium:latest -f ./client/Dockerfile.selenium ./client

echo "All images built successfully."