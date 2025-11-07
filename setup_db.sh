#!/bin/bash

# Shaaka Database Setup Script
# Quick script to set up just the database schema

echo "============================================================"
echo "📦 Shaaka Database Setup"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL is not installed${NC}"
    exit 1
fi

# Get MySQL password
echo -e "${YELLOW}Enter your MySQL root password:${NC}"
read -s MYSQL_PASSWORD
echo ""

# Create database
echo "Creating database..."
mysql -u root -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS farmer_market;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${RED}❌ Failed to create database${NC}"
    exit 1
fi

# Import main schema
if [ -f "database_schema.sql" ]; then
    echo "Importing main schema..."
    mysql -u root -p"$MYSQL_PASSWORD" farmer_market < database_schema.sql 2>/dev/null
    echo -e "${GREEN}✓ Main schema imported${NC}"
fi

# Import blog schema
if [ -f "add_blog_schema.sql" ]; then
    echo "Importing blog schema..."
    mysql -u root -p"$MYSQL_PASSWORD" farmer_market < add_blog_schema.sql 2>/dev/null
    echo -e "${GREEN}✓ Blog schema imported${NC}"
fi

# Import setup database (with reviews table)
if [ -f "setup_database.sql" ]; then
    echo "Importing additional tables..."
    mysql -u root -p"$MYSQL_PASSWORD" farmer_market < setup_database.sql 2>/dev/null
    echo -e "${GREEN}✓ Additional tables imported${NC}"
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Database setup complete!${NC}"
echo "============================================================"
echo ""
echo "To add test data, run: python3 setup_dummy_data.py"
echo ""
