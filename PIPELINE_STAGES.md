# Jenkins Pipeline Stages Documentation

This document describes the Jenkins pipeline stages used for the PasteBox CI/CD pipeline (see `Jenkinsfile`).

## Stage 1: Checkout & Initialize
- Purpose: Fetch source code and set Git metadata in the build environment.
- Actions: `checkout scm`, capture commit/branch metadata.
- Output: Source present in Jenkins workspace.

## Stage 2: Setup & Environment Verification
- Purpose: Verify required tools (Node, npm, Docker, docker-compose, Java).
- Actions: Print versions and basic environment diagnostics.
- Output: Environment verification logs.

## Stage 3: Backend Build
- Purpose: Install backend dependencies and prepare server for tests.
- Actions: `cd server && npm install`.
- Output: `node_modules` for server.

## Stage 4: Frontend Build
- Purpose: Build production client bundle.
- Actions: `cd client && npm install && npm run build`.
- Output: `client/dist` (or `client/dist`/`build`) ready for serving.

## Stage 5: Unit Testing - Backend
- Purpose: Run Jest unit tests and generate coverage.
- Actions: `cd server && npm test -- --coverage --watchAll=false`.
- Output: `server/test-results/test-results.xml`, `server/coverage/index.html`.

## Stage 6: Build Docker Images
- Purpose: Build container images for server, client, and Selenium test runner.
- Actions: `docker build -t pastebox-server:${BUILD_NUMBER} ./server`,
  `docker build -t pastebox-client:${BUILD_NUMBER} ./client`,
  `docker build -t pastebox-selenium:${BUILD_NUMBER} -f ./client/Dockerfile.selenium ./client`.
- Output: Docker images tagged with the build number.

## Stage 7: Containerized Deployment
- Purpose: Launch the multi-container stack using `docker-compose`.
- Actions: `docker-compose down && docker-compose up -d` and health checks.
- Output: Running containers and basic health verification.

## Stage 8: Containerized Selenium Testing
- Purpose: Run Selenium UI tests inside a container against the running stack.
- Actions: Run the Selenium image with network access to the compose network and mount `client/test-results` to collect `results.xml` and `report.html`.
- Expected artifacts: `client/test-results/results.xml`, `client/test-results/report.html`.

## Stage 9: Post-Deployment Validation
- Purpose: Verify container health and basic connectivity.
- Actions: Check `docker ps`, ping MongoDB from `server`, curl frontend/backend endpoints.
- Output: Validation logs and status.

## Stage 10: Cleanup & Optimization
- Purpose: Remove unused Docker images and free disk space.
- Actions: `docker image prune -f --filter "until=168h"` and disk checks.

---

Notes & Requirements:
- Jenkins agent must be a Linux node with Docker and docker-compose installed, and the Jenkins user must be allowed to run Docker.
- Ensure Jenkins credentials are configured for `mongodb-uri` and `jwt-secret` (or replace with environment-safe secrets).
- Node engine: Use Node 18–20 on the Jenkins agent to match `server/package.json` engines.
- If using a self-hosted Docker-in-Docker setup, ensure proper permissions and mount points for artifact collection.
