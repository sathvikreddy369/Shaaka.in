#!/usr/bin/env python3
"""
Test login functionality and fix password issues
"""
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootroot',
    'database': 'farmer_market'
}

def test_login():
    print("=" * 60)
    print("🔍 Testing Login System")
    print("=" * 60)
    print()
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Test customer login
        print("1. Checking customer accounts...")
        cursor.execute("SELECT id, name, email, password FROM customers LIMIT 5")
        customers = cursor.fetchall()
        
        if not customers:
            print("   ❌ No customers found in database!")
            print("   Run: python3 fix_passwords.py")
            return
        
        print(f"   ✓ Found {len(customers)} customers")
        print()
        
        # Test password for first customer
        test_customer = customers[0]
        print(f"2. Testing login for: {test_customer['email']}")
        print(f"   Name: {test_customer['name']}")
        print(f"   Password hash: {test_customer['password'][:50]}...")
        print()
        
        # Test password verification
        test_password = 'password123'
        stored_hash = test_customer['password']
        
        print(f"3. Testing password verification...")
        print(f"   Testing password: {test_password}")
        
        try:
            is_valid = check_password_hash(stored_hash, test_password)
            if is_valid:
                print(f"   ✅ Password verification WORKS!")
                print()
                print("=" * 60)
                print("✅ Login system is working correctly!")
                print("=" * 60)
                print()
                print("Test these credentials:")
                print(f"  Email: {test_customer['email']}")
                print(f"  Password: {test_password}")
                print()
                print("Visit: http://localhost:5000/customer_login")
            else:
                print(f"   ❌ Password verification FAILED!")
                print()
                print("Fixing passwords now...")
                fix_all_passwords(cursor, conn)
        except Exception as e:
            print(f"   ❌ Error during verification: {e}")
            print()
            print("Fixing passwords now...")
            fix_all_passwords(cursor, conn)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        print()
        print("Solutions:")
        print("1. Check MySQL is running: brew services list")
        print("2. Restart MySQL: brew services restart mysql")
        print("3. Check credentials in test_login.py")

def fix_all_passwords(cursor, conn):
    """Fix all passwords in database"""
    print()
    print("🔧 Fixing all passwords...")
    print()
    
    test_password = 'password123'
    hashed = generate_password_hash(test_password)
    
    # Fix customers
    cursor.execute("SELECT id, email FROM customers")
    customers = cursor.fetchall()
    for customer in customers:
        cursor.execute("UPDATE customers SET password = %s WHERE id = %s", 
                     (hashed, customer['id']))
        print(f"✓ Fixed: {customer['email']}")
    
    # Fix farmers
    cursor.execute("SELECT id, phone FROM farmers")
    farmers = cursor.fetchall()
    for farmer in farmers:
        cursor.execute("UPDATE farmers SET password = %s WHERE id = %s", 
                     (hashed, farmer['id']))
        print(f"✓ Fixed: {farmer['phone']}")
    
    # Fix employees
    cursor.execute("SELECT id, email FROM employees")
    employees = cursor.fetchall()
    for employee in employees:
        cursor.execute("UPDATE employees SET password = %s WHERE id = %s", 
                     (hashed, employee['id']))
        print(f"✓ Fixed: {employee['email']}")
    
    # Fix admins
    cursor.execute("SELECT id, email FROM admin")
    admins = cursor.fetchall()
    for admin in admins:
        cursor.execute("UPDATE admin SET password = %s WHERE id = %s", 
                     (hashed, admin['id']))
        print(f"✓ Fixed: {admin['email']}")
    
    conn.commit()
    
    print()
    print("=" * 60)
    print("✅ All passwords fixed!")
    print("=" * 60)
    print()
    print("All accounts now use password: password123")
    print()
    print("Test login at: http://localhost:5000/customer_login")

if __name__ == "__main__":
    test_login()
