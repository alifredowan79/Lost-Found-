#!/bin/bash
# Simple script to run the BUBT Lost and Found System

cd /media/alif-redwan/E/Code/Lost-Found-Prototype-main

echo "🚀 Starting BUBT Lost and Found System..."
echo ""
echo "📍 The application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "📝 Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""

# Run the application
python3 app.py

