#!/bin/bash

echo "🔧 Upgrading packages for Python 3.13 compatibility..."
echo ""

# Upgrade pip first
pip3 install --upgrade pip

# Install updated packages
pip3 install Flask==3.0.0
pip3 install Flask-Login==0.6.3
pip3 install Flask-WTF==1.2.1
pip3 install mysql-connector-python==9.1.0
pip3 install Werkzeug==3.0.1
pip3 install razorpay==1.4.2

echo ""
echo "✅ Packages upgraded successfully!"
echo ""
echo "Now run: python3 app.py"
