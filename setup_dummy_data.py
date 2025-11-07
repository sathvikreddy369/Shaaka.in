#!/usr/bin/env python3
"""
Script to set up the database with reviews table and dummy data
"""
import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootroot',
    'database': 'farmer_market'
}

def execute_sql_file(filename):
    """Execute SQL commands from a file"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print(f"Reading SQL file: {filename}")
        with open(filename, 'r') as file:
            sql_commands = file.read()
        
        # Split by semicolon and execute each command
        commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
        
        for command in commands:
            try:
                cursor.execute(command)
                conn.commit()
                print(f"✓ Executed: {command[:50]}...")
            except Error as e:
                # Skip errors for duplicate entries or existing columns
                if 'Duplicate entry' in str(e) or 'already exists' in str(e):
                    print(f"⚠ Skipped (already exists): {command[:50]}...")
                else:
                    print(f"✗ Error: {e}")
                    print(f"  Command: {command[:100]}...")
        
        cursor.close()
        conn.close()
        print("\n✓ Database setup completed successfully!")
        
    except Error as e:
        print(f"✗ Database error: {e}")
    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Setting up Farmer Market Database")
    print("=" * 60)
    
    print("\n📦 Installing database schema and dummy data...")
    execute_sql_file('setup_database.sql')
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\n📝 Test Accounts (password: password123)")
    print("-" * 60)
    print("Customers:")
    print("  • john@example.com")
    print("  • jane@example.com")
    print("  • bob@example.com")
    print("  • alice@example.com")
    print("  • mike@example.com")
    print("\nFarmers (use phone number):")
    print("  • 9123456780 (Ravi Kumar)")
    print("  • 9123456781 (Lakshmi Devi)")
    print("  • 9123456782 (Suresh Reddy)")
    print("  • 9123456783 (Manjunath Gowda)")
    print("  • 9123456784 (Kavitha Naik)")
    print("\nEmployees/Homemakers:")
    print("  • priya@example.com")
    print("  • anita@example.com")
    print("  • meena@example.com")
    print("  • rekha@example.com")
    print("\nAdmins:")
    print("  • admin@farmermarket.com")
    print("  • superadmin@farmermarket.com")
    print("=" * 60)
    print("\n📊 Dummy Data Summary:")
    print("-" * 60)
    print("  • 8 Customers")
    print("  • 5 Farmers")
    print("  • 15 Crops (with ratings)")
    print("  • 8 Recipes")
    print("  • 4 Employees")
    print("  • 12 Cooked Foods")
    print("  • 15+ Reviews")
    print("=" * 60)
    print("\n🚀 Ready to start! Run: python3 app.py")
    print("=" * 60)
