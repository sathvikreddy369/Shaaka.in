#!/bin/bash

# Seed Dummy Data Script for macOS/Linux
# This script imports sample data into the database

echo "========================================"
echo "   Shaaka - Seed Dummy Data"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if MySQL is installed
echo "Checking MySQL installation..."
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}[ERROR] MySQL is not installed or not in PATH.${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] MySQL found${NC}"
echo ""

# Get MySQL password
echo -e "${YELLOW}Enter your MySQL root password:${NC}"
read -s MYSQL_PASSWORD
echo ""

# Check if database exists
echo "Checking if database exists..."
mysql -u root -p"$MYSQL_PASSWORD" -e "USE farmer_market;" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Database 'farmer_market' does not exist.${NC}"
    echo "Please run setup.sh first to create the database."
    exit 1
fi
echo -e "${GREEN}[OK] Database found${NC}"
echo ""

# Import sample data
echo "========================================"
echo "   Importing Sample Data"
echo "========================================"
echo ""
echo "This will add:"
echo "  - Demo user accounts (Admin, Customer, Farmer, Homemaker)"
echo "  - 6 sample products (vegetables and fruits)"
echo "  - 4 sample food items (home-cooked meals)"
echo "  - 6 product reviews"
echo "  - 3 blog posts (already in add_blog_schema.sql)"
echo "  - 10 FAQs (already in add_blog_schema.sql)"
echo ""
echo -e "${YELLOW}[WARNING] This will add data to existing tables.${NC}"
echo "          Duplicate entries will be skipped."
echo ""
echo -e "${YELLOW}Continue with data import? (y/n)${NC}"
read -r CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Import cancelled."
    exit 0
fi

echo ""
echo "Importing sample data..."
mysql -u root -p"$MYSQL_PASSWORD" farmer_market < sample_data.sql 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] Sample data imported successfully!${NC}"
    echo ""
    echo "========================================"
    echo "   Demo Accounts Created"
    echo "========================================"
    echo ""
    echo "Admin Account:"
    echo "  URL:      http://localhost:5001/admin_login"
    echo "  Email:    admin@farmermarket.com"
    echo "  Password: password123"
    echo ""
    echo "Customer Account:"
    echo "  URL:      http://localhost:5001/customer_login"
    echo "  Email:    customer@example.com"
    echo "  Password: password123"
    echo ""
    echo "Farmer Account:"
    echo "  URL:      http://localhost:5001/login"
    echo "  Phone:    9876543220"
    echo "  Password: password123"
    echo ""
    echo "Homemaker Account:"
    echo "  URL:      http://localhost:5001/employee_login"
    echo "  Email:    homemaker@example.com"
    echo "  Password: password123"
    echo ""
    echo "========================================"
    echo "   Sample Data Summary"
    echo "========================================"
    echo "  - 4 user accounts"
    echo "  - 6 products (vegetables and fruits)"
    echo "  - 4 food items (home-cooked meals)"
    echo "  - 6 product reviews"
    echo "  - 3 blog posts"
    echo "  - 10 FAQs"
    echo ""
    echo -e "${GREEN}You can now login and test the application!${NC}"
else
    echo -e "${RED}[ERROR] Failed to import sample data.${NC}"
    echo "Please check:"
    echo "  1. MySQL password is correct"
    echo "  2. sample_data.sql file exists"
    echo "  3. Database tables are created"
    echo ""
    echo "Try running setup.sh first if you haven't already."
fi

echo ""
