# BUBT Lost & Found System - Server Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BUBT Lost & Found System" -ForegroundColor Cyan
Write-Host "  Starting Flask Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Flask is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Flask not found. Installing dependencies..." -ForegroundColor Yellow
        pip install Flask Flask-SQLAlchemy Werkzeug python-dotenv
    } else {
        Write-Host "✓ Dependencies OK" -ForegroundColor Green
    }
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install Flask Flask-SQLAlchemy Werkzeug python-dotenv
}

Write-Host ""
Write-Host "Starting server on http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python app.py

