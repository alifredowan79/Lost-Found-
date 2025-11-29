# 🚀 Render Deployment - Quick Start Guide

## Step-by-Step Instructions

### 1. Prepare Your Code

✅ All files are ready:
- `requirements.txt` ✓
- `Procfile` ✓
- `render.yaml` ✓ (optional, for easier setup)

### 2. Push to GitHub

```bash
# If not already a git repository
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/lostfound.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render

#### A. Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Settings:
   - **Name**: `lostfound-db`
   - **Database**: `lost_found`
   - **User**: `lostfound_user` (or leave default)
   - **Region**: Choose closest to you
   - **Plan**: **Free** (for testing)
4. Click **"Create Database"**
5. Wait for database to be ready (2-3 minutes)
6. **Copy these values** (you'll need them):
   - Internal Database URL (looks like: `postgresql://user:pass@host:5432/dbname`)
   - Or note down: Host, Port, Database, User, Password separately

#### B. Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account (if not already)
3. Select your repository: `lostfound`
4. Settings:
   - **Name**: `lostfound-app`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

#### C. Add Environment Variables

In the **"Environment"** section, click **"Add Environment Variable"** and add:

```
SECRET_KEY
```
Value: Generate a random string (you can use: https://randomkeygen.com/)

```
DATABASE_URL
```
Value: Paste the **Internal Database URL** from your PostgreSQL service

**OR** if you prefer individual variables:

```
DB_HOST
```
Value: From database settings (e.g., `dpg-xxxxx-a.oregon-postgres.render.com`)

```
DB_PORT
```
Value: `5432`

```
DB_NAME
```
Value: `lost_found` (or your database name)

```
DB_USER
```
Value: Your database user

```
DB_PASSWORD
```
Value: Your database password

```
USE_SQLITE
```
Value: `false`

#### D. Deploy

1. Click **"Create Web Service"**
2. Render will start building your app
3. Watch the build logs (takes 5-10 minutes first time)
4. Once deployed, you'll get a URL like: `https://lostfound-app.onrender.com`

### 4. Initialize Database

After deployment completes:

1. Visit: `https://your-app-url.onrender.com/init-db`
2. This will create all database tables
3. You should see: "Database initialized successfully!"

### 5. Test Your App

1. Visit your app URL
2. Try creating an account
3. Test login
4. Create a lost/found item

---

## 🔧 Troubleshooting

### Build Fails

**Error**: "Module not found"
- Check `requirements.txt` has all packages
- Check build logs for specific error

**Error**: "Command failed"
- Verify `startCommand` is: `gunicorn app:app`
- Check Python version (Render uses Python 3.11 by default)

### Database Connection Error

**Error**: "Could not connect to database"
- Verify `DATABASE_URL` is correct
- Check database is running (green status)
- Use **Internal Database URL** (not External)
- Verify `USE_SQLITE=false` is set

### App Crashes on Start

**Error**: "Application error"
- Check logs in Render dashboard
- Verify all environment variables are set
- Check `SECRET_KEY` is set

### 500 Internal Server Error

- Check application logs
- Verify database tables exist (visit `/init-db`)
- Check environment variables

---

## 📝 Important Notes

1. **Free Tier Limitations**:
   - App sleeps after 15 minutes of inactivity
   - First request after sleep takes 30-60 seconds
   - Database has 90MB storage limit (free tier)

2. **Upgrade to Paid**:
   - $7/month for always-on service
   - Better performance
   - More database storage

3. **Custom Domain**:
   - Free tier supports custom domains
   - Add in "Settings" → "Custom Domain"

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL database created
- [ ] Web service created
- [ ] Environment variables set
- [ ] Build successful
- [ ] Database initialized (`/init-db`)
- [ ] App tested and working

---

## 🎉 Success!

Your app is now live! Share the URL with others.

**Need help?** Check Render docs: https://render.com/docs

