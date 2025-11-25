# PostgreSQL Integration Guide

## ✅ PostgreSQL Database Integration

The application now supports PostgreSQL database with SQLite as fallback.

## Installation

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

**Start PostgreSQL service:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Install Python Dependencies

```bash
pip3 install --break-system-packages -r requirements.txt
```

Or install manually:
```bash
pip3 install --break-system-packages psycopg2-binary python-dotenv
```

### 3. Create PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE lost_found;
CREATE USER lost_found_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE lost_found TO lost_found_user;
ALTER USER lost_found_user CREATEDB;
\q
```

### 4. Configure Environment Variables

**Option A: Using .env file (Recommended)**

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lost_found
DB_USER=lost_found_user
DB_PASSWORD=your_secure_password
SECRET_KEY=your-secret-key-change-in-production
```

**Option B: Using Environment Variables**

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=lost_found
export DB_USER=lost_found_user
export DB_PASSWORD=your_secure_password
export SECRET_KEY=your-secret-key
```

**Option C: Using Full Connection String**

```bash
export DATABASE_URL=postgresql://lost_found_user:password@localhost:5432/lost_found
```

### 5. Initialize Database

```bash
python3 -c "from app import init_db; init_db()"
```

Or the database will be automatically created when you run the app for the first time.

## Configuration Priority

The app checks for database configuration in this order:

1. `DATABASE_URL` environment variable (full connection string)
2. Individual `DB_*` environment variables
3. `.env` file
4. SQLite fallback (if PostgreSQL not configured)

## Testing Connection

```bash
python3 -c "
from app import app, db
with app.app_context():
    try:
        db.engine.connect()
        print('✅ PostgreSQL connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
"
```

## Migration from SQLite to PostgreSQL

If you have existing SQLite data:

1. **Export data from SQLite:**
```bash
sqlite3 lost_found.db .dump > backup.sql
```

2. **Import to PostgreSQL:**
```bash
psql -U lost_found_user -d lost_found < backup.sql
```

Or use a migration tool like Flask-Migrate.

## Common Issues

### Issue 1: "psycopg2 not found"
**Solution:**
```bash
pip3 install --break-system-packages psycopg2-binary
```

### Issue 2: "Connection refused"
**Solution:**
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Check firewall settings
- Verify connection details in `.env`

### Issue 3: "Authentication failed"
**Solution:**
- Verify username and password
- Check `pg_hba.conf` for authentication method
- Ensure user has proper permissions

### Issue 4: "Database does not exist"
**Solution:**
```bash
sudo -u postgres createdb lost_found
```

## Production Setup

For production, use environment variables or a secure configuration management system:

```bash
# Set in your deployment environment
export DATABASE_URL=postgresql://user:pass@host:5432/dbname
export SECRET_KEY=your-very-secure-secret-key
```

## Connection Pooling

The app is configured with connection pooling:
- `pool_pre_ping`: Checks connections before using
- `pool_recycle`: Recycles connections after 300 seconds
- `connect_timeout`: 10 seconds timeout

## Backup and Restore

**Backup:**
```bash
pg_dump -U lost_found_user lost_found > backup.sql
```

**Restore:**
```bash
psql -U lost_found_user lost_found < backup.sql
```

## Monitoring

Check database connections:
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'lost_found';
```

## Notes

- The app will automatically fallback to SQLite if PostgreSQL is not configured
- All database models work the same with PostgreSQL
- No code changes needed - just configuration
- PostgreSQL provides better performance and features for production

