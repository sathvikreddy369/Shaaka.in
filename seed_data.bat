@echo off
REM Seed Dummy Data Script for Windows
REM This script imports sample data into the database

echo ========================================
echo    Shaaka - Seed Dummy Data
echo ========================================
echo.

REM Check if MySQL is installed
echo Checking MySQL installation...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] MySQL is not installed or not in PATH.
    pause
    exit /b 1
)
echo [OK] MySQL found
echo.

REM Get MySQL password
set /p MYSQL_PASSWORD="Enter your MySQL root password: "
echo.

REM Check if database exists
echo Checking if database exists...
mysql -u root -p%MYSQL_PASSWORD% -e "USE farmer_market;" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Database 'farmer_market' does not exist.
    echo Please run setup.bat first to create the database.
    pause
    exit /b 1
)
echo [OK] Database found
echo.

REM Import sample data
echo ========================================
echo    Importing Sample Data
echo ========================================
echo.
echo This will add:
echo   - Demo user accounts (Admin, Customer, Farmer, Homemaker)
echo   - 6 sample products (vegetables and fruits)
echo   - 4 sample food items (home-cooked meals)
echo   - 6 product reviews
echo   - 3 blog posts (already in add_blog_schema.sql)
echo   - 10 FAQs (already in add_blog_schema.sql)
echo.
echo [WARNING] This will add data to existing tables.
echo           Duplicate entries will be skipped.
echo.
set /p CONFIRM="Continue with data import? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Import cancelled.
    pause
    exit /b 0
)

echo.
echo Importing sample data...
mysql -u root -p%MYSQL_PASSWORD% farmer_market < sample_data.sql 2>nul
if %errorlevel% equ 0 (
    echo [OK] Sample data imported successfully!
    echo.
    echo ========================================
    echo    Demo Accounts Created
    echo ========================================
    echo.
    echo Admin Account:
    echo   URL:      http://localhost:5001/admin_login
    echo   Email:    admin@farmermarket.com
    echo   Password: password123
    echo.
    echo Customer Account:
    echo   URL:      http://localhost:5001/customer_login
    echo   Email:    customer@example.com
    echo   Password: password123
    echo.
    echo Farmer Account:
    echo   URL:      http://localhost:5001/login
    echo   Phone:    9876543220
    echo   Password: password123
    echo.
    echo Homemaker Account:
    echo   URL:      http://localhost:5001/employee_login
    echo   Email:    homemaker@example.com
    echo   Password: password123
    echo.
    echo ========================================
    echo    Sample Data Summary
    echo ========================================
    echo   - 4 user accounts
    echo   - 6 products (vegetables and fruits)
    echo   - 4 food items (home-cooked meals)
    echo   - 6 product reviews
    echo   - 3 blog posts
    echo   - 10 FAQs
    echo.
    echo You can now login and test the application!
) else (
    echo [ERROR] Failed to import sample data.
    echo Please check:
    echo   1. MySQL password is correct
    echo   2. sample_data.sql file exists
    echo   3. Database tables are created
    echo.
    echo Try running setup.bat first if you haven't already.
)

echo.
pause
