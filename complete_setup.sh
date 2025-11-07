#!/bin/bash

echo "============================================================"
echo "🚀 Complete Shaaka Setup"
echo "============================================================"
echo ""

# Step 1: Fix database schema
echo "Step 1/2: Fixing database schema..."
echo ""
./fix_db.sh

echo ""
echo "============================================================"
echo ""

# Step 2: Fix passwords
echo "Step 2/2: Fixing passwords..."
echo ""
python3 fix_passwords.py

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "🎉 Everything is ready! Run: python3 app.py"
echo ""
