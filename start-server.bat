@echo off
title BUBT Lost and Found - Flask Server
color 0A
echo ========================================
echo   BUBT Lost and Found System
echo   Starting Flask Server...
echo ========================================
echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b 1
)
echo.
echo Checking Flask...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing dependencies...
    pip install Flask Flask-SQLAlchemy Werkzeug python-dotenv
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo.
echo ========================================
echo   Server Starting...
echo ========================================
echo.
echo Server will be available at:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
python app.py
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Check the error messages above.
    pause
)

