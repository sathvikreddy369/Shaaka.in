#!/bin/bash

echo "=========================================="
echo "Farmer Market - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if MySQL is running
if ! pgrep -x "mysqld" > /dev/null; then
    echo "⚠️  MySQL doesn't appear to be running. Please start MySQL first."
    echo "   On Mac: brew services start mysql"
    echo "   On Linux: sudo systemctl start mysql"
    exit 1
fi

echo "✓ MySQL is running"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q mysql-connector-python==9.1.0 Flask==2.2.3 Flask-Login==0.6.2 Werkzeug==2.2.3

# Setup database
echo ""
echo "🗄️  Setting up database..."
python3 setup_dummy_data.py

# Run the application
echo ""
echo "=========================================="
echo "🚀 Starting Farmer Market Application..."
echo "=========================================="
echo ""
echo "Visit: http://localhost:5000"
echo ""
echo "Test Accounts (password: password123):"
echo "  Customer: john@example.com"
echo "  Farmer: 9123456780"
echo "  Homemaker: priya@example.com"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
