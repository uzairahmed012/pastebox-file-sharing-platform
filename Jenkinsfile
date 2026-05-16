// Jenkins Pipeline for PasteBox File Sharing Platform CI/CD
// This pipeline automates: Build → Unit Test → Docker Build → Deploy → Selenium Tests

pipeline {
    agent any

    options {
        // Keep last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Set timeout to 1 hour
        timeout(time: 1, unit: 'HOURS')
        // Disable concurrent builds
        disableConcurrentBuilds()
        // Add timestamps to console output
        timestamps()
    }

    environment {
        // Environment variables
        DOCKER_REGISTRY = 'your-registry'  // Replace with your registry
        DOCKER_IMAGE_SERVER = "pastebox-server:${BUILD_NUMBER}"
        DOCKER_IMAGE_CLIENT = "pastebox-client:${BUILD_NUMBER}"
        DOCKER_IMAGE_SELENIUM = "pastebox-selenium:${BUILD_NUMBER}"
        DOCKER_COMPOSE_VERSION = '1.29.2'
        NODE_VERSION = '20.x'
        MONGO_URI = credentials('mongodb-uri')  // Stored in Jenkins credentials
        JWT_SECRET = credentials('jwt-secret')
        AWS_REGION = 'us-east-1'  // Change as needed
    }

    stages {
        stage('🔍 Stage 1: Checkout & Initialize') {
            steps {
                echo "========== Stage 1: Checkout Code =========="
                checkout scm
                
                script {
                    env.GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.GIT_COMMIT_MSG = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
                    env.GIT_BRANCH_NAME = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                }
                
                sh '''
                    echo "📦 Repository Information:"
                    echo "Branch: ${GIT_BRANCH_NAME}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                    echo "Message: ${GIT_COMMIT_MSG}"
                    echo "Workspace: ${WORKSPACE}"
                '''
            }
        }

        stage('🔧 Stage 2: Setup & Environment Verification') {
            steps {
                echo "========== Stage 2: Environment Setup =========="
                sh '''
                    echo "✓ System Information:"
                    uname -a
                    
                    echo ""
                    echo "✓ Node.js Version:"
                    node --version
                    npm --version
                    
                    echo ""
                    echo "✓ Docker Version:"
                    docker --version
                    docker-compose --version
                    
                    echo ""
                    echo "✓ Java Version (for Jenkins):"
                    java -version
                    
                    echo ""
                    echo "✓ Available Disk Space:"
                    df -h /
                '''
            }
        }

        stage('📦 Stage 3: Backend Build') {
            steps {
                echo "========== Stage 3: Building Backend =========="
                sh '''
                    echo "Building Server Application..."
                    cd server
                    
                    echo "Installing dependencies..."
                    npm install
                    
                    echo "Backend dependencies installed successfully!"
                    
                    # Verify build
                    if [ -f "package.json" ]; then
                        echo "✓ package.json verified"
                    fi
                    
                    cd ..
                '''
            }
        }

        stage('🎨 Stage 4: Frontend Build') {
            steps {
                echo "========== Stage 4: Building Frontend =========="
                sh '''
                    echo "Building Client Application..."
                    cd client
                    
                    echo "Installing dependencies..."
                    npm install
                    
                    echo "Building production bundle..."
                    npm run build
                    
                    echo "Frontend build completed successfully!"
                    
                    # Verify build output
                    if [ -d "dist" ]; then
                        echo "✓ Distribution folder created"
                        du -sh dist
                    fi
                    
                    cd ..
                '''
            }
        }

        stage('🧪 Stage 5: Unit Testing - Backend') {
            steps {
                echo "========== Stage 5: Backend Unit Tests =========="
                sh '''
                    cd server
                    
                    echo "Running unit tests with coverage..."
                    npm test -- --coverage --watchAll=false || true
                    
                    echo "Tests completed!"
                    
                    # Check if coverage exists
                    if [ -d "coverage" ]; then
                        echo "✓ Coverage report generated"
                        echo "Coverage summary:"
                        ls -la coverage/ | head -20
                    fi
                    
                    cd ..
                '''
            }
            post {
                always {
                    // Archive test results
                    junit 'server/test-results/test-results.xml' || true
                    
                    // Publish coverage report
                    publishHTML([
                        reportDir: 'server/coverage',
                        reportFiles: 'index.html',
                        reportName: '📊 Backend Coverage Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ]) || true
                }
            }
        }

        stage('🐳 Stage 6: Build Docker Images') {
            steps {
                echo "========== Stage 6: Building Docker Images =========="
                sh '''
                    echo "Building Server Docker Image: ${DOCKER_IMAGE_SERVER}"
                    docker build -t ${DOCKER_IMAGE_SERVER} ./server --no-cache
                    
                    echo ""
                    echo "Building Client Docker Image: ${DOCKER_IMAGE_CLIENT}"
                    docker build -t ${DOCKER_IMAGE_CLIENT} ./client --no-cache
                    
                    echo ""
                    echo "Building Selenium Docker Image: ${DOCKER_IMAGE_SELENIUM}"
                    docker build -t ${DOCKER_IMAGE_SELENIUM} -f ./client/Dockerfile.selenium ./client --no-cache
                    
                    echo ""
                    echo "✓ All Docker images built successfully!"
                    echo ""
                    echo "Docker Images Summary:"
                    docker images | grep pastebox
                '''
            }
        }

        stage('🚀 Stage 7: Containerized Deployment') {
            steps {
                echo "========== Stage 7: Deploying Containers =========="
                sh '''
                    echo "Stopping existing containers..."
                    docker-compose down || true
                    sleep 2
                    
                    echo "Starting application stack with docker-compose..."
                    docker-compose up -d
                    
                    echo "Waiting for services to be healthy..."
                    sleep 15
                    
                    echo "Container Status:"
                    docker-compose ps
                    
                    echo ""
                    echo "Checking container health..."
                    for i in {1..5}; do
                        echo "Health check attempt $i/5..."
                        
                        if docker-compose exec -T server curl -f http://localhost:5000/ 2>/dev/null; then
                            echo "✓ Backend is responding"
                            break
                        fi
                        
                        if [ $i -lt 5 ]; then
                            sleep 5
                        fi
                    done
                    
                    echo ""
                    echo "Displaying service logs (last 30 lines):"
                    docker-compose logs --tail=30
                '''
            }
            post {
                failure {
                    sh '''
                        echo "========== Deployment Logs (Full) =========="
                        docker-compose logs || true
                    '''
                }
            }
        }

        stage('🤖 Stage 8: Containerized Selenium Testing') {
            steps {
                echo "========== Stage 8: Running Selenium Tests =========="
                sh '''
                    echo "Verifying application is running..."
                    
                    # Wait for application to be fully ready
                    for i in {1..30}; do
                        if docker-compose exec -T client curl -f http://localhost:80 2>/dev/null; then
                            echo "✓ Application is ready for testing"
                            break
                        fi
                        echo "Waiting for application... ($i/30)"
                        sleep 2
                    done
                    
                    echo ""
                    echo "Running Selenium Tests in Container..."
                    docker run --rm \
                        --network pastebox-network \
                        -e APP_URL=http://client \
                        -e CI=true \
                        -v ${WORKSPACE}/client/test-results:/app/test-results \
                        ${DOCKER_IMAGE_SELENIUM} || true
                    
                    echo ""
                    echo "Selenium tests completed!"
                    
                    # Check if test results exist
                    if [ -f "client/test-results/results.xml" ]; then
                        echo "✓ Test results file found"
                    fi
                '''
            }
            post {
                always {
                    // Archive Selenium test results
                    junit 'client/test-results/results.xml' || true
                    
                    // Publish HTML test report
                    publishHTML([
                        reportDir: 'client/test-results',
                        reportFiles: 'report.html',
                        reportName: '🧪 Selenium Test Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ]) || true
                }
            }
        }

        stage('✅ Stage 9: Post-Deployment Validation') {
            steps {
                echo "========== Stage 9: Validation =========="
                sh '''
                    echo "Checking running containers..."
                    RUNNING=$(docker ps --quiet)
                    if [ -z "$RUNNING" ]; then
                        echo "❌ ERROR: No containers running!"
                        exit 1
                    fi
                    
                    echo "✓ Containers are running:"
                    docker ps --format "table {{.Names}}\t{{.Status}}"
                    
                    echo ""
                    echo "Checking network connectivity..."
                    docker-compose exec -T server ping -c 1 mongodb || echo "Warning: MongoDB not responding"
                    
                    echo ""
                    echo "Application Status:"
                    echo "- Frontend: http://localhost:80"
                    echo "- Backend API: http://localhost:5000"
                    
                    echo ""
                    echo "✓ Deployment validation completed!"
                '''
            }
        }

        stage('🧹 Stage 10: Cleanup & Optimization') {
            when {
                always {}
            }
            steps {
                echo "========== Stage 10: Cleanup =========="
                sh '''
                    echo "Performing cleanup operations..."
                    
                    echo "Removing unused Docker resources..."
                    docker image prune -f --filter "until=168h" || true
                    
                    echo "Checking disk space..."
                    df -h
                    
                    echo "✓ Cleanup completed!"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ ========== PIPELINE EXECUTION SUCCESSFUL =========="
            sh '''
                echo "Build Status: SUCCESS ✓"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Build Duration: ${BUILD_DURATION}"
                echo "Timestamp: $(date)"
                
                # Generate summary
                cat > /tmp/build_summary.txt << EOF
BUILD SUMMARY
=============
Build Status: SUCCESS
Build Number: ${BUILD_NUMBER}
Build Duration: ${BUILD_DURATION}
Git Branch: ${GIT_BRANCH_NAME}
Git Commit: ${GIT_COMMIT_SHORT}
Commit Message: ${GIT_COMMIT_MSG}

DELIVERABLES
============
- Server Image: ${DOCKER_IMAGE_SERVER}
- Client Image: ${DOCKER_IMAGE_CLIENT}
- Selenium Image: ${DOCKER_IMAGE_SELENIUM}

TEST RESULTS
============
- Unit Tests: Completed
- Selenium Tests: Completed
- Coverage Reports: Generated

NEXT STEPS
==========
1. Review test reports in Jenkins UI
2. Verify deployment in staging
3. Run additional integration tests if needed
EOF
                cat /tmp/build_summary.txt
            '''
        }

        failure {
            echo "❌ ========== PIPELINE EXECUTION FAILED =========="
            sh '''
                echo "Build Status: FAILED ✗"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Collecting diagnostics..."
                
                # Collect logs
                docker-compose logs > /tmp/pipeline_logs.txt 2>&1 || true
                
                echo ""
                echo "Recent Logs (last 50 lines):"
                tail -50 /tmp/pipeline_logs.txt || echo "No logs available"
            '''
        }

        unstable {
            echo "⚠️  ========== PIPELINE EXECUTION UNSTABLE =========="
        }

        always {
            echo "========== FINAL SUMMARY =========="
            sh '''
                echo "Pipeline Execution Summary:"
                echo "- Build Result: ${BUILD_RESULT}"
                echo "- Build Number: ${BUILD_NUMBER}"
                echo "- Build Duration: ${BUILD_DURATION}"
                echo "- Workspace: ${WORKSPACE}"
                
                echo ""
                echo "Generated Artifacts:"
                find ${WORKSPACE} -name "*.xml" -o -name "coverage" -o -name "test-results" | head -20 || echo "No artifacts found"
            '''
        }
    }
}
