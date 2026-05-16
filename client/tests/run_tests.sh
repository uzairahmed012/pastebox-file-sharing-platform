#!/bin/bash

# PasteBox Selenium Test Runner
# Runs Selenium tests with HTML and XML reports

set -e

echo "=========================================="
echo "PasteBox Selenium Test Suite"
echo "=========================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLIENT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to client directory
cd "$CLIENT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Python version:${NC}"
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create test results directory
mkdir -p test-results

# Run tests with reports
echo -e "${YELLOW}Running Selenium tests...${NC}"
echo "=========================================="

pytest tests/ \
    -v \
    --tb=short \
    --html=test-results/report.html \
    --self-contained-html \
    --junit-xml=test-results/results.xml \
    --maxfail=10 \
    --disable-warnings \
    "$@"

TEST_RESULT=$?

# Deactivate virtual environment
deactivate

echo "=========================================="

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed!${NC}"
fi

# Display test results summary
if [ -f "test-results/report.html" ]; then
    echo -e "${YELLOW}Test report generated:${NC} test-results/report.html"
fi

if [ -f "test-results/results.xml" ]; then
    echo -e "${YELLOW}Test results XML:${NC} test-results/results.xml"
fi

exit $TEST_RESULT
