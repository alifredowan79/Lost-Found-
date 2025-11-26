# Quick PostgreSQL Setup Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Install PostgreSQL & pgAdmin
1. Download from: https://www.postgresql.org/download/windows/
2. During installation:
   - **Remember your PostgreSQL password** (for `postgres` user)
   - Install **pgAdmin 4** (comes with PostgreSQL)
   - Default port: `5432`

### Step 2: Create Database in pgAdmin
1. Open **pgAdmin 4**
2. Connect to server (password you set during installation)
3. Right-click **Databases** → **Create** → **Database**
   - Name: `lost_found`
   - Click **Save**

### Step 3: Configure Your App
1. Edit `.env` file in your project folder:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=lost_found
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password_here
   SECRET_KEY=your-secret-key-here
   ```
   **Replace `your_postgres_password_here` with your actual PostgreSQL password!**

2. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```
   
   If that fails, try:
   ```bash
   pip install psycopg2
   ```

3. Run your app:
   ```bash
   python app.py
   ```

## ✅ Verify Connection

When you run `python app.py`, you should see:
```
✅ Connected to PostgreSQL database: lost_found on localhost:5432
```

## 🔗 Connect with pgAdmin

1. Open **pgAdmin 4**
2. Expand: **Servers** → **PostgreSQL** → **Databases** → **lost_found**
3. You can now:
   - View all tables (users, items, invoices)
   - Run SQL queries
   - Manage data directly

## 🆘 Troubleshooting

**"psycopg2-binary installation failed"**
- Install Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use: `pip install psycopg2`

**"Connection refused"**
- Check if PostgreSQL service is running (Windows Services)
- Verify port 5432 is correct

**"Authentication failed"**
- Check your password in `.env` file
- Make sure it matches your PostgreSQL password

**"Database does not exist"**
- Create the database first in pgAdmin (see Step 2)

