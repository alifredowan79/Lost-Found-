# প্রজেক্ট চালু করার নির্দেশিকা (Installation Guide)

## সমস্যা: pip ইনস্টল নেই

আপনার সিস্টেমে `pip` ইনস্টল নেই। নিচের ধাপগুলো অনুসরণ করুন:

## সমাধান ১: pip ইনস্টল করুন

টার্মিনালে এই কমান্ডগুলো চালান:

```bash
# pip ইনস্টল করুন
sudo apt update
sudo apt install python3-pip -y

# pip ভার্সন চেক করুন
pip3 --version
```

## সমাধান ২: Dependencies ইনস্টল করুন

pip ইনস্টল হওয়ার পর:

```bash
# প্রজেক্ট ফোল্ডারে যান
cd /media/alif-redwan/E/Code/Lost-Found-Prototype-main

# Dependencies ইনস্টল করুন
pip3 install -r requirements.txt

# অথবা সরাসরি ইনস্টল করুন
pip3 install Flask Flask-SQLAlchemy Werkzeug
```

## সমাধান ৩: প্রজেক্ট চালু করুন

```bash
# প্রজেক্ট চালু করুন
python3 app.py
```

তারপর ব্রাউজারে যান: `http://localhost:5000`

## Alternative: Virtual Environment ব্যবহার করুন (সুপারিশকৃত)

```bash
# Virtual environment তৈরি করুন
python3 -m venv venv

# Virtual environment চালু করুন
source venv/bin/activate

# pip ইনস্টল করুন (venv এর মধ্যে)
python -m ensurepip --upgrade

# Dependencies ইনস্টল করুন
pip install -r requirements.txt

# প্রজেক্ট চালু করুন
python app.py
```

## যদি pip ইনস্টল করতে সমস্যা হয়

যদি `sudo apt install python3-pip` কাজ না করে, তাহলে:

```bash
# get-pip.py ডাউনলোড করুন
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# pip ইনস্টল করুন
python3 get-pip.py

# pip চেক করুন
pip3 --version
```

## Login Credentials

প্রজেক্ট চালু হওয়ার পর এই credentials দিয়ে login করুন:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`
- Username: `test@bubt.edu.bd`, Password: `test123`

## সমস্যা হলে

যদি কোনো error দেখেন, error message টি আমাকে জানান।

