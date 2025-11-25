# Quick Start Guide (দ্রুত শুরু করার নির্দেশিকা)

## সমস্যা: প্রজেক্ট চালু করতে পারছেন না?

### সমাধান ১: pip ইনস্টল করুন

টার্মিনালে এই কমান্ড চালান:

```bash
sudo apt update
sudo apt install python3-pip -y
```

### সমাধান ২: Dependencies ইনস্টল করুন

**Option A: Otomatic installer ব্যবহার করুন**
```bash
python3 install_dependencies.py
```

**Option B: Manual ইনস্টল করুন**
```bash
pip3 install Flask Flask-SQLAlchemy Werkzeug
```

**Option C: requirements.txt থেকে ইনস্টল করুন**
```bash
pip3 install -r requirements.txt
```

### সমাধান ৩: প্রজেক্ট চালু করুন

**Option A: run.sh script ব্যবহার করুন (সবচেয়ে সহজ)**
```bash
./run.sh
```

**Option B: সরাসরি Python দিয়ে চালু করুন**
```bash
python3 app.py
```

### ব্রাউজারে খুলুন

প্রজেক্ট চালু হওয়ার পর:
- URL: `http://localhost:5000`
- Login করুন demo credentials দিয়ে

## Demo Login Credentials

- **Username:** `admin` | **Password:** `admin123`
- **Username:** `user` | **Password:** `user123`
- **Username:** `test@bubt.edu.bd` | **Password:** `test123`

## যদি এখনও সমস্যা হয়

1. Error message টি কপি করুন
2. `INSTALL_GUIDE_BN.md` ফাইলটি দেখুন
3. অথবা আমাকে error message টি জানান

## সহায়ক ফাইল

- `INSTALL_GUIDE_BN.md` - বিস্তারিত ইনস্টলেশন গাইড
- `run.sh` - সহজে প্রজেক্ট চালু করার script
- `install_dependencies.py` - Otomatic dependency installer

