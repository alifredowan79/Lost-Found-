# User Password Management Guide

## ⚠️ Important Security Note
**Passwords are hashed and cannot be viewed or decrypted.** This is for security. However, you can:
- View user information
- Reset passwords
- Test if a password is correct

## 📋 View All Users

```bash
python view_users.py list
```

This will show:
- User ID
- Username
- Email
- Password Hash (hashed, cannot be decrypted)
- Created date

## 👤 View Specific User

```bash
python view_users.py view redowan.alif
```

## 🔐 Test Password

To check if a password is correct for a user:

```bash
python view_users.py test redowan.alif redwan1234
```

## 🔄 Reset Password

To change a user's password:

```bash
python reset_user_password.py reset redowan.alif newpassword123
```

## 📝 Default Users and Passwords

Based on the code, default users are:

1. **admin**
   - Username: `admin`
   - Password: `admin123`
   - Email: `admin@bubt.edu.bd`

2. **user**
   - Username: `user`
   - Password: `user123`
   - Email: `user@bubt.edu.bd`

3. **test**
   - Username: `test`
   - Password: `test123`
   - Email: `test@bubt.edu.bd`

4. **redowan.alif**
   - Username: `redowan.alif`
   - Password: `redwan1234` (recently reset)
   - Email: `redowan.alif@bubt.edu.bd`

## 🔍 View in pgAdmin

You can also view users directly in pgAdmin:

1. Open pgAdmin 4
2. Connect to your PostgreSQL server
3. Navigate to: `Databases` → `lost_found` → `Schemas` → `public` → `Tables` → `userid`
4. Right-click on `userid` → `View/Edit Data` → `All Rows`

**Note:** You'll see the `password_hash` column, but it's hashed and cannot be decrypted.

## 🛠️ Quick Commands Summary

```bash
# View all users
python view_users.py list

# View specific user
python view_users.py view <username>

# Test password
python view_users.py test <username> <password>

# Reset password
python reset_user_password.py reset <username> <new_password>

# Check user exists
python reset_user_password.py check <username>
```


