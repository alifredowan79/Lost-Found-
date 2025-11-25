#!/bin/bash
# PostgreSQL Setup Script for BUBT Lost and Found System

echo "=========================================="
echo "PostgreSQL Setup for Lost & Found System"
echo "=========================================="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed!"
    echo ""
    echo "Installing PostgreSQL..."
    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
    
    if [ $? -eq 0 ]; then
        echo "✅ PostgreSQL installed successfully!"
    else
        echo "❌ Failed to install PostgreSQL"
        exit 1
    fi
else
    echo "✅ PostgreSQL is already installed"
fi

# Start PostgreSQL service
echo ""
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Get database configuration
echo ""
read -p "Enter database name [lost_found]: " DB_NAME
DB_NAME=${DB_NAME:-lost_found}

read -p "Enter database user [lost_found_user]: " DB_USER
DB_USER=${DB_USER:-lost_found_user}

read -sp "Enter database password: " DB_PASSWORD
echo ""

read -p "Enter database host [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Enter database port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

# Create database and user
echo ""
echo "Creating database and user..."
sudo -u postgres psql << EOF
-- Create database
CREATE DATABASE $DB_NAME;

-- Create user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER USER $DB_USER CREATEDB;

-- Connect to database and grant schema privileges
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database and user created successfully!"
else
    echo "❌ Failed to create database/user"
    exit 1
fi

# Create .env file
echo ""
echo "Creating .env file..."
cat > .env << EOF
# PostgreSQL Database Configuration
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

# Secret Key for Flask sessions
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
EOF

echo "✅ .env file created successfully!"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install --break-system-packages psycopg2-binary python-dotenv

# Initialize database
echo ""
echo "Initializing database tables..."
python3 -c "from app import init_db; init_db()"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ PostgreSQL setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Database Configuration:"
    echo "  Host: $DB_HOST"
    echo "  Port: $DB_PORT"
    echo "  Database: $DB_NAME"
    echo "  User: $DB_USER"
    echo ""
    echo "You can now run the application:"
    echo "  python3 app.py"
    echo ""
else
    echo "❌ Failed to initialize database"
    exit 1
fi

