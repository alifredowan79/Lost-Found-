#!/bin/bash
# Simple run script for BUBT Lost and Found System

echo "BUBT Lost and Found System - Starting..."
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo ""
    echo "Please install pip3 first:"
    echo "  sudo apt update"
    echo "  sudo apt install python3-pip -y"
    echo ""
    echo "Or see INSTALL_GUIDE_BN.md for detailed instructions"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install Flask Flask-SQLAlchemy Werkzeug
    echo ""
fi

# Check if database exists, if not initialize
if [ ! -f "lost_found.db" ]; then
    echo "🗄️  Initializing database..."
    python3 -c "from app import init_db; init_db()" 2>/dev/null || echo "Database will be created on first run"
    echo ""
fi

# Run the application
echo "🚀 Starting Flask application..."
echo "📍 Open your browser: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""
python3 app.py

