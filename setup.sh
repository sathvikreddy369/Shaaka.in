#!/bin/bash

# Shaaka Platform Setup Script for macOS/Linux
# This script automates the setup process

echo "============================================================"
echo "🌾 Welcome to Shaaka Platform Setup"
echo "============================================================"
echo "Connecting local vendors and homemakers with customers"
echo "Fresh produce and homemade food delivered to your door"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if MySQL is installed
echo "Checking MySQL installation..."
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL is not installed. Please install MySQL 8.0 or higher.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ MySQL found${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Database setup
echo ""
echo "Setting up database..."
echo -e "${YELLOW}Please enter your MySQL root password:${NC}"
read -s MYSQL_PASSWORD

# Create database
echo "Creating database..."
mysql -u root -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS farmer_market;" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${RED}❌ Failed to create database. Please check your MySQL password.${NC}"
    exit 1
fi

# Import schema
echo "Importing database schema..."
mysql -u root -p"$MYSQL_PASSWORD" farmer_market < database_schema.sql 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database schema imported${NC}"
else
    echo -e "${RED}❌ Failed to import schema. Make sure database_schema.sql exists.${NC}"
fi

# Import blog schema
echo "Importing blog and FAQ schema..."
mysql -u root -p"$MYSQL_PASSWORD" farmer_market < add_blog_schema.sql 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Blog and FAQ schema imported${NC}"
else
    echo -e "${YELLOW}⚠ Blog schema import failed. You may need to run it manually.${NC}"
fi

# Import sample data
echo ""
echo "========================================"
echo "Sample Data Import"
echo "========================================"
echo ""
echo "Sample data includes:"
echo "  - 8 Customer accounts"
echo "  - 5 Vendor accounts (selling fresh produce)"
echo "  - 4 Homemaker accounts (selling homemade food)"
echo "  - 15 Products (vegetables, fruits, grains)"
echo "  - 12 Homemade food items"
echo "  - 20+ Product reviews with ratings"
echo "  - 8 Recipes"
echo "  - 2 Admin accounts"
echo ""
echo -e "${YELLOW}Do you want to import sample/dummy data for testing? (y/n)${NC}"
read -r IMPORT_SAMPLE
if [ "$IMPORT_SAMPLE" = "y" ] || [ "$IMPORT_SAMPLE" = "Y" ]; then
    echo ""
    echo "Importing sample data..."
    mysql -u root -p"$MYSQL_PASSWORD" farmer_market < sample_data.sql 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Sample data imported successfully!${NC}"
        echo ""
        echo "Demo Accounts Created (password: password123):"
        echo "  Admin:     admin@shaaka.com"
        echo "  Customer:  john@example.com (or jane, bob, alice, mike, etc.)"
        echo "  Vendor:    9123456780 (Ravi Kumar - use phone to login)"
        echo "  Homemaker: priya@example.com"
    else
        echo -e "${YELLOW}⚠ Sample data import failed. You can import it manually later.${NC}"
        echo "Run: mysql -u root -p farmer_market < sample_data.sql"
    fi
else
    echo -e "${YELLOW}[INFO] Skipping sample data import.${NC}"
    echo "You can import it later by running:"
    echo "  mysql -u root -p farmer_market < sample_data.sql"
fi

# Update database credentials in app.py
echo ""
echo "Updating database credentials in app.py..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/'password': 'rootroot'/'password': '$MYSQL_PASSWORD'/g" app.py
else
    # Linux
    sed -i "s/'password': 'rootroot'/'password': '$MYSQL_PASSWORD'/g" app.py
fi
echo -e "${GREEN}✓ Database credentials updated${NC}"

# Create uploads directory
echo ""
echo "Creating uploads directory..."
mkdir -p static/uploads
echo -e "${GREEN}✓ Uploads directory created${NC}"

# Setup complete
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📝 Test Login Credentials (password: password123):"
echo "   Admin:     admin@shaaka.com"
echo "   Customer:  john@example.com"
echo "   Vendor:    9123456780 (use phone number)"
echo "   Homemaker: priya@example.com"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the application: python3 app.py"
echo "   3. Open browser: http://localhost:5000"
echo ""
echo "📚 For more information, see README.md"
echo "💡 Run 'python3 setup_dummy_data.py' to see all test accounts"
echo ""

# Ask if user wants to start the application now
echo -e "${YELLOW}Do you want to start the application now? (y/n)${NC}"
read -r START_APP
if [ "$START_APP" = "y" ] || [ "$START_APP" = "Y" ]; then
    echo ""
    echo "Starting Shaaka application..."
    echo "Press Ctrl+C to stop the server"
    echo ""
    python app.py
fi
