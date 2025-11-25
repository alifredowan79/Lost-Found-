# 🚀 How to Run Your Lost & Found Project

This guide will help you run your BUBT Lost & Found System project. You have **two options**:

## 📋 **Option 1: Run as Flask Application (Recommended - Full Features)**

This runs the complete application with database support and all backend features.

### **Prerequisites:**
- Python 3.7 or higher
- pip (Python package manager)

### **Step-by-Step Instructions:**

#### **1. Open Terminal/Command Prompt**
- **Windows**: Press `Win + R`, type `cmd` or `powershell`, press Enter
- **Mac/Linux**: Open Terminal

#### **2. Navigate to Project Directory**
```bash
cd D:\Code\Lost-Found-Prototype-main
```

#### **3. Activate Virtual Environment (if exists)**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

#### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **5. Run the Application**
```bash
python app.py
```

#### **6. Open in Browser**
- Open your web browser
- Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
- You should see the login page!

### **Default Credentials (if database is set up):**
- Username: `admin`
- Password: `admin123`

---

## 📄 **Option 2: Run as Static HTML Files (Quick Testing)**

This runs only the frontend without backend features. Good for testing UI/UX.

### **Method A: Direct File Opening**
1. Navigate to project folder: `D:\Code\Lost-Found-Prototype-main`
2. Double-click `login.html` or `index.html`
3. It will open in your default browser

### **Method B: Using Python HTTP Server**
1. Open Terminal/Command Prompt in project directory
2. Run:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Or Python 2
   python -m SimpleHTTPServer 8000
   ```
3. Open browser: `http://localhost:8000/login.html`

### **Method C: Using VS Code Live Server**
1. Install "Live Server" extension in VS Code
2. Right-click on `login.html`
3. Select "Open with Live Server"

---

## 🔧 **Troubleshooting**

### **Problem: "Module not found" error**
**Solution:**
```bash
pip install Flask Flask-SQLAlchemy Werkzeug psycopg2-binary python-dotenv
```

### **Problem: "Port already in use"**
**Solution:** Change the port in `app.py`:
```python
app.run(port=5001)  # Use different port
```

### **Problem: Database connection error**
**Solution:** The app will automatically use SQLite if PostgreSQL is not configured. Check `app.py` for database configuration.

### **Problem: Scripts not loading**
**Solution:** Make sure `login-script.js` exists in the root directory. If not, copy it from `static/js/login-script.js`.

---

## 📁 **Project Structure**

```
Lost-Found-Prototype-main/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── login.html            # Login page
├── dashboard.html        # Dashboard page
├── login-script.js       # Login page JavaScript
├── login-styles.css      # Login page styles
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/           # Flask templates
└── instance/            # Database files
```

---

## ✅ **Quick Start Commands**

**For Flask (Full Application):**
```bash
cd D:\Code\Lost-Found-Prototype-main
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**For Static HTML (Quick Test):**
```bash
cd D:\Code\Lost-Found-Prototype-main
python -m http.server 8000
```

Then open: `http://localhost:8000/login.html`

---

## 🎯 **What to Expect**

1. **Login Page** - Modern, dynamic login interface
2. **Dashboard** - After login, you'll see the main dashboard
3. **Features Available:**
   - Report Lost Items
   - Report Found Items
   - Search Items
   - Generate Invoices
   - View Statistics

---

## 💡 **Tips**

- **First Time?** Start with Option 2 (Static HTML) to see the UI quickly
- **Full Features?** Use Option 1 (Flask) for complete functionality
- **Development?** Use VS Code Live Server for auto-refresh
- **Production?** Use Flask with proper database setup

---

## 🆘 **Need Help?**

If you encounter any issues:
1. Check that all files are in the correct locations
2. Verify Python version: `python --version`
3. Check if dependencies are installed: `pip list`
4. Look at the terminal/console for error messages

---

**Happy Coding! 🎉**

