# Lost and Found Management System

A comprehensive web application for managing lost and found items, built with Flask and PostgreSQL.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Database Information](#database-information)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Item Management**: Create, search, and manage lost/found items
- **Admin Panel**: Admin users can manage all users and items
- **Real-time Dashboard**: Live statistics and recent activity
- **Search Functionality**: Advanced search with filters (category, status, date, location)
- **Report System**: Report lost or found items with detailed information
- **Student Information**: Track student ID, program (BSC, BBA, MBA, MCS, etc.), and department
- **Responsive Design**: Modern UI with purple gradient theme

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download PostgreSQL](https://www.postgresql.org/download/))
- **pgAdmin 4** (Optional, for database management) ([Download pgAdmin](https://www.pgadmin.org/download/))
- **pip** (Python package manager)

## 📦 Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd LostFound

# Or extract the project folder
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Werkzeug==3.0.1
- python-dotenv==1.0.0
- psycopg2-binary==2.9.9
- gunicorn==21.2.0

## 🗄️ Database Setup

### Step 1: Install PostgreSQL

1. Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. During installation, remember the password you set for the `postgres` user
3. PostgreSQL will run on port `5432` by default

### Step 2: Create Database

Open **pgAdmin 4** or **psql** command line:

```sql
-- Connect to PostgreSQL
-- Open pgAdmin 4, right-click on "Databases" > Create > Database

-- Or use psql command line:
psql -U postgres

-- Create the database
CREATE DATABASE lost_found;

-- Verify database creation
\l
```

### Step 3: Verify Database Connection

```bash
# Test connection using psql
psql -U postgres -d lost_found -h localhost -p 5432
```

## ⚙️ Configuration

### Step 1: Create `.env` File

Create a `.env` file in the project root directory:

```env
# Database Configuration (PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lost_found
DB_USER=postgres
DB_PASSWORD=your_postgres_password

# Secret Key (Change this in production!)
SECRET_KEY=your-secret-key-change-in-production

# Optional: Full Database URL (alternative to individual variables)
# DATABASE_URL=postgresql://postgres:password@localhost:5432/lost_found
```

### Step 2: Update Database Credentials

Replace the following values in `.env`:
- `DB_PASSWORD`: Your PostgreSQL password
- `SECRET_KEY`: A random secret key for Flask sessions

**Important:** Never commit the `.env` file to version control!

## 🚀 Running the Project

### Step 1: Initialize Database

```bash
# Run the application once to create tables
python app.py
```

This will:
- Create all database tables (`userid`, `item`, `lost_found_item`)
- Create default admin user (if not exists)
- Set up the database schema

### Step 2: Start the Application

```bash
python app.py
```

The application will start on:
- **URL**: `http://localhost:5000`
- **Port**: 5000 (default)

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 🗃️ Database Information

### Database Name
```
lost_found
```

### Database Tables

#### 1. `userid` Table
- Stores user authentication information
- **Columns**: `id`, `username`, `email`, `password_hash`, `remember_me`, `created_at`, `is_admin`

#### 2. `item` Table
- Stores main item catalog (created by admin)
- **Primary Key**: `name`
- **Columns**: 
  - `name` (Primary Key) - Item Name *
  - `category` - Category *
  - `date` - Date *
  - `description` - Description *
  - `color` (optional) - Color
  - `brand` (optional) - Brand/Model
  - `value` (optional) - Estimated Value

#### 3. `lost_found_item` Table
- Stores reported lost/found items
- **Primary Key**: `id`
- **Foreign Key**: `name` references `item.name`
- **Columns**:
  - `id` (Primary Key)
  - `name` (Foreign Key to `item.name`)
  - `category`, `date`, `location`, `description`
  - `contact`, `phone`, `student_id`
  - `program` (BSC, BBA, MBA, MCS, etc.)
  - `department`
  - `status` ('lost' or 'found')
  - `created_at`, `updated_at`

### Database Connection Details

**PostgreSQL Connection:**
```
Host: localhost
Port: 5432
Database: lost_found
User: postgres
Password: [Your PostgreSQL password]
```

**Connection String Format:**
```
postgresql://postgres:password@localhost:5432/lost_found
```

### Connect Using pgAdmin

1. Open **pgAdmin 4**
2. Right-click on **Servers** > **Create** > **Server**
3. Enter connection details:
   - **Name**: Lost Found DB (or any name)
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `lost_found`
   - **Username**: `postgres`
   - **Password**: Your PostgreSQL password
4. Click **Save**

## 📁 Project Structure

```
LostFound/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
├── README.md                   # This file
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Dashboard
│   ├── create-item.html       # Create item (Admin only)
│   ├── search.html            # Search items
│   ├── report.html            # Report lost/found items
│   ├── about.html             # About page
│   └── admin_files.html       # Admin panel
│
└── static/                     # Static files
    ├── css/                   # Stylesheets
    │   ├── styles.css
    │   ├── login-styles.css
    │   ├── dashboard-styles.css
    │   ├── create-item-styles.css
    │   ├── search-styles.css
    │   ├── report-styles.css
    │   └── about-styles.css
    └── js/                    # JavaScript files
        ├── script.js
        └── login-script.js
```

## 👥 User Roles

### Admin User
- Can create items in the main catalog
- Can view all users and their passwords in Admin Files
- Can reset user passwords
- Has access to all features

### Regular User
- Can search for items
- Can report lost/found items
- Can view dashboard and statistics
- Cannot create items (admin only)

### Default Admin Account
On first run, a default admin user is created:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

**⚠️ Important:** Change the default admin password after first login!

## 🔌 API Endpoints

### Authentication
- `GET /` - Welcome/Login page
- `POST /login` - User login
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - User logout

### Main Features
- `GET /dashboard` - Dashboard (requires login)
- `GET /create-item` - Create item page (Admin only)
- `POST /create-item` - Create new item (Admin only)
- `GET /search` - Search items page
- `GET /report` - Report lost/found page
- `POST /report` - Submit lost/found report
- `GET /about` - About page with statistics

### Admin
- `GET /admin/files` - Admin panel (Admin only)
- `POST /admin/files` - Reset user password (Admin only)

### API
- `GET /api/stats` - Get dashboard statistics (JSON)
- `GET /api/search` - Search items API (JSON)

## 🐛 Troubleshooting

### Database Connection Issues

**Error: `psycopg2.OperationalError: could not connect to server`**

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   # Windows
   services.msc  # Check PostgreSQL service

   # Linux
   sudo systemctl status postgresql
   ```

2. Check `.env` file credentials:
   - Verify `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
   - Ensure no extra spaces or quotes

3. Test connection manually:
   ```bash
   psql -U postgres -d lost_found -h localhost -p 5432
   ```

### Module Not Found Errors

**Error: `ModuleNotFoundError: No module named 'psycopg2'`**

**Solution:**
```bash
pip install psycopg2-binary
```

### Port Already in Use

**Error: `Address already in use`**

**Solution:**
```bash
# Change port in app.py or set environment variable
set PORT=5001  # Windows
export PORT=5001  # Linux/Mac
python app.py
```

### Database Tables Not Created

**Solution:**
```bash
# Run initialization
python app.py

# Or manually initialize
python -c "from app import init_db; init_db()"
```

### Environment Variables Not Loading

**Solution:**
1. Ensure `.env` file exists in project root
2. Check file name is exactly `.env` (not `.env.txt`)
3. Verify `python-dotenv` is installed: `pip install python-dotenv`

## 📝 Additional Notes

### Database Configuration
The application requires PostgreSQL database. Configuration is checked in this order:
1. `DATABASE_URL` environment variable (full connection string)
2. Individual PostgreSQL variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`)

**Note:** PostgreSQL is required. SQLite is not supported.

### Security Notes
- Passwords are stored in **plain text** (for admin visibility)
- Change `SECRET_KEY` in production
- Use HTTPS in production
- Never commit `.env` file to version control

### Development vs Production
- **Development**: Debug mode enabled, runs on `localhost:5000`
- **Production**: Use `gunicorn` or similar WSGI server
  ```bash
  gunicorn app:app
  ```

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify database connection and credentials
3. Check application logs for error messages
4. Ensure all dependencies are installed

## 📄 License

This project is for educational purposes.

---

**Last Updated:** 2024
**Version:** 1.0.0

