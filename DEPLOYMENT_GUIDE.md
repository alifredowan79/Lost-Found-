# Deployment Guide - Lost & Found App

## 🚀 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Render** is the easiest and most beginner-friendly platform for Flask apps.

#### Steps:

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/lostfound.git
   git push -u origin main
   ```

2. **Sign up at Render**
   - Go to https://render.com
   - Sign up with your GitHub account

3. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `lostfound-db`
   - Plan: Free
   - Click "Create Database"
   - Copy the **Internal Database URL** (you'll need this)

4. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `lostfound-app`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

5. **Add Environment Variables**
   In the "Environment" section, add:
   ```
   SECRET_KEY=your-secret-key-here (generate a random string)
   DB_HOST=your-db-host-from-render
   DB_PORT=5432
   DB_NAME=lost_found
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   USE_SQLITE=false
   ```
   
   Or use the **Internal Database URL**:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app
   - Wait for deployment to complete (5-10 minutes)

7. **Initialize Database**
   - Once deployed, visit: `https://your-app.onrender.com/init-db`
   - This will create the database tables

---

### Option 2: Railway (Alternative - Free Tier)

1. **Sign up at Railway**: https://railway.app
2. **Create New Project** → "Deploy from GitHub repo"
3. **Add PostgreSQL** service
4. **Add Environment Variables**:
   - `SECRET_KEY` (generate random string)
   - `DATABASE_URL` (auto-provided by Railway)
5. **Deploy** - Railway auto-detects Flask apps

---

### Option 3: Heroku (Paid - $5/month minimum)

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create lostfound-app`
4. **Add PostgreSQL**: `heroku addons:create heroku-postgresql:mini`
5. **Set environment variables**: `heroku config:set SECRET_KEY=your-secret-key`
6. **Deploy**: `git push heroku main`
7. **Initialize DB**: `heroku run python -c "from app import init_db; init_db()"`

---

## 📝 Important Notes

### Before Deploying:

1. **Update app.py for Production**
   ```python
   if __name__ == '__main__':
       init_db()
       # Remove debug=True for production
       app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
   ```

2. **Install Gunicorn** (already in requirements.txt)
   - Gunicorn is a production WSGI server

3. **Environment Variables**
   - Never commit `.env` file to GitHub
   - Add `.env` to `.gitignore`
   - Set all variables in the hosting platform

4. **Database Migration**
   - After first deployment, visit `/init-db` to create tables
   - Or run: `python -c "from app import init_db; init_db()"`

### Security Checklist:

- ✅ Change `SECRET_KEY` to a random string
- ✅ Use PostgreSQL (not SQLite) in production
- ✅ Set `USE_SQLITE=false`
- ✅ Don't commit `.env` file
- ✅ Use HTTPS (most platforms provide automatically)

---

## 🔧 Troubleshooting

### Database Connection Issues:
- Check environment variables are set correctly
- Verify database is running
- Check database credentials

### App Not Starting:
- Check build logs in Render/Railway dashboard
- Verify `requirements.txt` is correct
- Check `startCommand` uses `gunicorn app:app`

### 500 Errors:
- Check application logs
- Verify database tables are created
- Check environment variables

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Flask Deployment: https://flask.palletsprojects.com/en/latest/deploying/

