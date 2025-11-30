#!/bin/bash

# Eli's Clothing Brand - One-Command Launcher
# This script builds and runs the containerized Flask application

set -e

echo "🛍️ Eli's Clothing Brand - Docker Launcher"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build the Docker image
echo -e "${BLUE}Building Docker image...${NC}"
docker build -t clothing-store:latest .

echo ""
echo -e "${GREEN}✓ Build complete!${NC}"
echo ""
echo -e "${BLUE}Starting container on port 8080...${NC}"
echo ""

# Run the container
docker run --rm \
    -p 8080:8080 \
    --env-file .env \
    --name clothing-store \
    clothing-store:latest

echo ""
echo -e "${GREEN}✓ Container running at http://localhost:8080${NC}"
