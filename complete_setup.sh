#!/bin/bash

# Shaaka Complete Setup Script
# This script sets up the entire database with dummy data

echo "============================================================"
echo "🚀 Shaaka Complete Setup"
echo "============================================================"
echo "Setting up database with test data for development"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL is not installed${NC}"
    exit 1
fi

# Run the setup script
echo "Running database setup with dummy data..."
echo ""
python3 setup_dummy_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}✅ Setup Complete!${NC}"
    echo "============================================================"
    echo ""
    echo "🎉 Database is ready with test data!"
    echo ""
    echo "🚀 To start the application:"
    echo "   python3 app.py"
    echo ""
    echo "🌐 Then open: http://localhost:5000"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Setup failed. Please check the error messages above.${NC}"
    exit 1
fi
