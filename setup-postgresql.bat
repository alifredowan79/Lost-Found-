@echo off
title PostgreSQL Setup for BUBT Lost & Found
color 0B
echo ========================================
echo   PostgreSQL Setup Script
echo   BUBT Lost and Found System
echo ========================================
echo.

echo Step 1: Checking PostgreSQL installation...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not installed or not in PATH!
    echo.
    echo Please install PostgreSQL from:
    echo https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
) else (
    echo [OK] PostgreSQL is installed
    psql --version
)
echo.

echo Step 2: Installing Python dependencies...
echo Installing psycopg2-binary...
pip install psycopg2-binary
if errorlevel 1 (
    echo.
    echo [WARNING] psycopg2-binary installation failed.
    echo Trying alternative: psycopg2
    pip install psycopg2
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install PostgreSQL driver!
        echo.
        echo You may need to install Visual C++ Build Tools:
        echo https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo.
        pause
        exit /b 1
    )
)
echo.

echo Step 3: Creating .env file...
if exist .env (
    echo [INFO] .env file already exists
    echo Do you want to overwrite it? (Y/N)
    set /p overwrite=
    if /i not "%overwrite%"=="Y" (
        echo Skipping .env file creation...
        goto :config
    )
)

echo.
echo Please provide your PostgreSQL credentials:
echo.
set /p DB_HOST="Database Host [localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT="Database Port [5432]: "
if "%DB_PORT%"=="" set DB_PORT=5432

set /p DB_NAME="Database Name [lost_found]: "
if "%DB_NAME%"=="" set DB_NAME=lost_found

set /p DB_USER="Database User [postgres]: "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_PASSWORD="Database Password: "

echo.
echo Creating .env file...
(
    echo # PostgreSQL Database Configuration
    echo DB_HOST=%DB_HOST%
    echo DB_PORT=%DB_PORT%
    echo DB_NAME=%DB_NAME%
    echo DB_USER=%DB_USER%
    echo DB_PASSWORD=%DB_PASSWORD%
    echo SECRET_KEY=your-secret-key-change-in-production
) > .env

echo [OK] .env file created successfully!
echo.

:config
echo Step 4: Testing database connection...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Testing connection to:', os.getenv('DB_HOST'), ':', os.getenv('DB_PORT'))"
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure PostgreSQL is running
echo 2. Create the database 'lost_found' in pgAdmin if not exists
echo 3. Run: python app.py
echo.
echo For detailed instructions, see: POSTGRESQL_SETUP.md
echo.
pause

