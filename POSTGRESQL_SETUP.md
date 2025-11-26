# PostgreSQL Setup Guide for BUBT Lost & Found System

## Step 1: Install PostgreSQL

### Windows:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. During installation:
   - Remember the password you set for the `postgres` user
   - Default port is `5432` (keep this)
   - Install pgAdmin 4 (comes with PostgreSQL)

### Verify Installation:
```bash
psql --version
```

## Step 2: Create Database in PostgreSQL

### Method 1: Using pgAdmin (GUI)
1. Open **pgAdmin 4**
2. Connect to your PostgreSQL server:
   - Right-click on "Servers" → "Create" → "Server"
   - **General Tab:**
     - Name: `BUBT Server` (or any name)
   - **Connection Tab:**
     - Host: `localhost`
     - Port: `5432`
     - Username: `postgres`
     - Password: (your PostgreSQL password)
   - Click "Save"
3. Create Database:
   - Expand your server → Right-click "Databases" → "Create" → "Database"
   - **Database:** `lost_found`
   - **Owner:** `postgres`
   - Click "Save"

### Method 2: Using Command Line (psql)
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE lost_found;

# Exit
\q
```

## Step 3: Configure Your Application

1. **Create `.env` file** in your project root:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=lost_found
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   SECRET_KEY=your-secret-key-here
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install psycopg2-binary
   ```
   
   If `psycopg2-binary` fails to install (needs Visual C++), try:
   ```bash
   pip install psycopg2
   ```
   
   Or use the pre-compiled wheel:
   ```bash
   pip install psycopg2-binary --only-binary :all:
   ```

## Step 4: Test Connection

Run your Flask app:
```bash
python app.py
```

You should see:
```
✅ Connected to PostgreSQL database: lost_found
```

## Step 5: Connect with pgAdmin

1. Open **pgAdmin 4**
2. Your server should already be connected (from Step 2)
3. Expand: `Servers` → `Your Server` → `Databases` → `lost_found`
4. You can now:
   - View tables
   - Run SQL queries
   - Manage data

## Troubleshooting

### Error: "psycopg2-binary installation failed"
**Solution:** Install Visual C++ Build Tools or use:
```bash
pip install psycopg2
```

### Error: "Connection refused"
**Solution:** 
- Check if PostgreSQL service is running
- Verify port 5432 is not blocked by firewall
- Check `DB_HOST` and `DB_PORT` in `.env`

### Error: "Authentication failed"
**Solution:**
- Verify username and password in `.env`
- Check PostgreSQL authentication settings in `pg_hba.conf`

### Error: "Database does not exist"
**Solution:**
- Create the database first (see Step 2)
- Verify `DB_NAME` in `.env` matches the created database

## Default Users Created

After running the app, these default users will be created:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`
- Username: `test`, Password: `test123`
- Username: `redowan.alif`, Password: `password123`

