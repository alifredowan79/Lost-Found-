# PostgreSQL Quick Start (দ্রুত শুরু)

## সহজ উপায় (Automatic Setup)

```bash
./setup_postgresql.sh
```

এই script automatically:
- PostgreSQL install করবে (যদি না থাকে)
- Database এবং user তৈরি করবে
- .env file তৈরি করবে
- Dependencies install করবে
- Database initialize করবে

## Manual Setup (যদি script কাজ না করে)

### 1. PostgreSQL Install করুন

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
```

### 2. Database তৈরি করুন

```bash
sudo -u postgres psql
```

PostgreSQL prompt-এ:
```sql
CREATE DATABASE lost_found;
CREATE USER lost_found_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE lost_found TO lost_found_user;
\q
```

### 3. .env File তৈরি করুন

```bash
cp .env.example .env
nano .env
```

`.env` file-এ এই values দিন:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lost_found
DB_USER=lost_found_user
DB_PASSWORD=your_password
SECRET_KEY=your-secret-key
```

### 4. Dependencies Install করুন

```bash
pip3 install --break-system-packages psycopg2-binary python-dotenv
```

### 5. Database Initialize করুন

```bash
python3 -c "from app import init_db; init_db()"
```

### 6. App চালু করুন

```bash
python3 app.py
```

## Connection Test করুন

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

## যদি PostgreSQL configure না করেন

App automatically SQLite ব্যবহার করবে। কোনো সমস্যা হবে না!

## Troubleshooting

### "psycopg2 not found"
```bash
pip3 install --break-system-packages psycopg2-binary
```

### "Connection refused"
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### "Authentication failed"
- Password check করুন
- User permissions verify করুন

## Production Setup

Production-এ environment variables ব্যবহার করুন:
```bash
export DATABASE_URL=postgresql://user:pass@host:5432/dbname
export SECRET_KEY=your-secure-key
```

