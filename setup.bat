@echo off
REM Shaaka Platform Setup Script for Windows
REM This script automates the setup process

echo ========================================
echo    Shaaka Platform Setup for Windows
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check if MySQL is installed
echo Checking MySQL installation...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] MySQL is not installed. Please install MySQL 8.0 or higher.
    pause
    exit /b 1
)
echo [OK] MySQL found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Database setup
echo ========================================
echo    Database Setup
echo ========================================
echo.
set /p MYSQL_PASSWORD="Enter your MySQL root password: "
echo.

REM Create database
echo Creating database...
mysql -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS farmer_market;" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Database created
) else (
    echo [ERROR] Failed to create database. Please check your MySQL password.
    pause
    exit /b 1
)

REM Import schema
echo Importing database schema...
mysql -u root -p%MYSQL_PASSWORD% farmer_market < database_schema.sql 2>nul
if %errorlevel% equ 0 (
    echo [OK] Database schema imported
) else (
    echo [ERROR] Failed to import schema. Make sure database_schema.sql exists.
)

REM Import blog schema
echo Importing blog and FAQ schema...
mysql -u root -p%MYSQL_PASSWORD% farmer_market < add_blog_schema.sql 2>nul
if %errorlevel% equ 0 (
    echo [OK] Blog and FAQ schema imported
) else (
    echo [WARNING] Blog schema import failed. You may need to run it manually.
)

REM Import sample data
echo.
set /p IMPORT_SAMPLE="Do you want to import sample data for testing? (Y/N): "
if /i "%IMPORT_SAMPLE%"=="Y" (
    echo Importing sample data...
    mysql -u root -p%MYSQL_PASSWORD% farmer_market < sample_data.sql 2>nul
    if %errorlevel% equ 0 (
        echo [OK] Sample data imported
    ) else (
        echo [WARNING] Sample data import failed. You can import it manually later.
    )
)
echo.

REM Update database credentials in app.py
echo Updating database credentials in app.py...
powershell -Command "(gc app.py) -replace \"'password': 'rootroot'\", \"'password': '%MYSQL_PASSWORD%'\" | Out-File -encoding ASCII app.py"
echo [OK] Database credentials updated
echo.

REM Create uploads directory
echo Creating uploads directory...
if not exist static\uploads mkdir static\uploads
echo [OK] Uploads directory created
echo.

REM Setup complete
echo ========================================
echo    Setup Completed Successfully!
echo ========================================
echo.
echo Default Login Credentials:
echo    Admin:     admin@farmermarket.com / password123
echo    Customer:  customer@example.com / password123
echo    Farmer:    farmer@example.com / password123
echo    Homemaker: homemaker@example.com / password123
echo.
echo To start the application:
echo    1. Activate virtual environment: venv\Scripts\activate
echo    2. Run the application: python app.py
echo    3. Open browser: http://localhost:5001
echo.
echo For more information, see README.md
echo.

REM Ask if user wants to start the application now
set /p START_APP="Do you want to start the application now? (Y/N): "
if /i "%START_APP%"=="Y" (
    echo.
    echo Starting Shaaka application...
    echo Press Ctrl+C to stop the server
    echo.
    python app.py
)

pause
