#!/bin/bash

# Hugging Face Spaces Deployment Script
# Usage: ./deploy_to_huggingface.sh YOUR_USERNAME your-space-name

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Hugging Face Spaces Deployment Script${NC}"
echo "=========================================="

# Check arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo "Usage: ./deploy_to_huggingface.sh YOUR_USERNAME your-space-name"
    echo "Example: ./deploy_to_huggingface.sh Gunalan183 apple-leaf-classifier"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME=$2
SPACE_URL="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

echo -e "${YELLOW}Target Space:${NC} ${SPACE_URL}"
echo ""

# Step 1: Check if model checkpoint exists
echo -e "${YELLOW}Step 1:${NC} Checking model checkpoint..."
if [ ! -f "ml-training/checkpoints/densenet121_best.pth" ]; then
    echo -e "${RED}Error: Model checkpoint not found!${NC}"
    echo "Please place densenet121_best.pth in ml-training/checkpoints/"
    exit 1
fi
echo -e "${GREEN}✓ Model checkpoint found${NC}"

# Step 2: Install Git LFS
echo -e "${YELLOW}Step 2:${NC} Setting up Git LFS..."
git lfs install
git lfs track "*.pth"
git lfs track "ml-training/checkpoints/*.pth"
echo -e "${GREEN}✓ Git LFS configured${NC}"

# Step 3: Build frontend
echo -e "${YELLOW}Step 3:${NC} Building frontend..."
cd frontend
npm install
VITE_API_URL=/api npm run build
cd ..
echo -e "${GREEN}✓ Frontend built${NC}"

# Step 4: Add Hugging Face remote
echo -e "${YELLOW}Step 4:${NC} Configuring Git remote..."
if git remote | grep -q "^space$"; then
    echo "Remote 'space' already exists, updating URL..."
    git remote set-url space https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}
else
    git remote add space https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}
fi
echo -e "${GREEN}✓ Remote configured${NC}"

# Step 5: Commit changes
echo -e "${YELLOW}Step 5:${NC} Committing deployment files..."
git add .gitattributes
git add app.py requirements.txt Dockerfile .spacesconfig
git add backend/app/config.py
git add frontend/dist/
git add frontend/.env.production
git add ml-training/checkpoints/densenet121_best.pth
git add README_DEPLOYMENT.md

git commit -m "Deploy to Hugging Face Spaces" || echo "No changes to commit"
echo -e "${GREEN}✓ Changes committed${NC}"

# Step 6: Push to Hugging Face
echo -e "${YELLOW}Step 6:${NC} Pushing to Hugging Face Spaces..."
echo "This may take a few minutes for large files..."
git push space main

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo -e "Your app will be available at:"
echo -e "${GREEN}${SPACE_URL}${NC}"
echo ""
echo -e "It may take 5-10 minutes for the build to complete."
echo -e "Check build logs at: ${SPACE_URL}/logs"
echo ""
