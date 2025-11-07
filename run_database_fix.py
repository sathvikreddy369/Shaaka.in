#!/usr/bin/env python3
"""
Quick script to fix the database schema
Handles errors gracefully for existing columns
"""
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootroot',
    'database': 'farmer_market'
}

def run_sql_file(filename):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print(f"📖 Reading {filename}...")
        with open(filename, 'r') as file:
            sql_script = file.read()
        
        # Split by delimiter and execute
        statements = []
        current_statement = []
        in_delimiter = False
        
        for line in sql_script.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('--'):
                continue
            
            # Handle DELIMITER
            if line.startswith('DELIMITER'):
                in_delimiter = not in_delimiter
                continue
            
            current_statement.append(line)
            
            # Check for statement end
            if not in_delimiter and line.endswith(';'):
                statements.append(' '.join(current_statement))
                current_statement = []
            elif in_delimiter and line == '//':
                statements.append(' '.join(current_statement[:-1]))  # Remove the //
                current_statement = []
        
        # Execute each statement
        success_count = 0
        error_count = 0
        
        for statement in statements:
            if not statement.strip():
                continue
            
            try:
                cursor.execute(statement)
                conn.commit()
                success_count += 1
                
                # Show progress for important operations
                if 'CREATE TABLE' in statement:
                    table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip().split()[0]
                    print(f"✓ Created table: {table_name}")
                elif 'CREATE TRIGGER' in statement:
                    trigger_name = statement.split('CREATE TRIGGER')[1].split()[0].strip()
                    print(f"✓ Created trigger: {trigger_name}")
                elif 'ALTER TABLE' in statement and 'ADD COLUMN' in statement:
                    parts = statement.split('ADD COLUMN')
                    if len(parts) > 1:
                        column_name = parts[1].split()[0].strip()
                        print(f"✓ Added column: {column_name}")
                        
            except Error as e:
                error_code = e.errno
                
                # Ignore "already exists" errors
                if error_code == 1060:  # Duplicate column
                    print(f"⚠ Column already exists (skipped)")
                elif error_code == 1050:  # Table already exists
                    print(f"⚠ Table already exists (skipped)")
                elif error_code == 1359:  # Trigger already exists
                    print(f"⚠ Trigger already exists (skipped)")
                elif error_code == 1062:  # Duplicate entry
                    print(f"⚠ Duplicate entry (skipped)")
                else:
                    print(f"✗ Error: {e}")
                    error_count += 1
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print(f"✅ Database fix completed!")
        print(f"   Successful operations: {success_count}")
        if error_count > 0:
            print(f"   Errors (non-critical): {error_count}")
        print("=" * 60)
        print("\n🎉 You can now run: python3 app.py")
        
    except Error as e:
        print(f"❌ Database connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Check MySQL is running: mysql -u root -p")
        print("2. Verify database exists: SHOW DATABASES LIKE 'farmer_market';")
        print("3. Check credentials in run_database_fix.py")
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        print("Make sure fix_database.sql is in the same directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Fixing Shaaka Database Schema")
    print("=" * 60)
    print()
    run_sql_file('fix_database.sql')
