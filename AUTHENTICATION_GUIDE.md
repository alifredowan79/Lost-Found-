# Authentication System Guide

## ✅ Python-based Authentication Implemented

The login authentication system has been fully converted to Python/Flask backend.

## Features

### 1. **User Authentication**
- ✅ Password hashing using Werkzeug (bcrypt)
- ✅ Username or Email login support
- ✅ Session management
- ✅ Remember me functionality (30 days)
- ✅ Secure password storage

### 2. **User Registration**
- ✅ New user registration route (`/register`)
- ✅ Input validation
- ✅ Duplicate username/email checking
- ✅ Password confirmation
- ✅ Automatic password hashing

### 3. **Session Management**
- ✅ Flask sessions for authentication
- ✅ Session timeout handling
- ✅ Remember me option
- ✅ Secure logout

### 4. **Protected Routes**
- ✅ All routes check for authentication
- ✅ Flash messages for unauthorized access
- ✅ Automatic redirect to login page

## Default Users

The system automatically creates these users on first run:

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@bubt.edu.bd | admin123 |
| user | user@bubt.edu.bd | user123 |
| test | test@bubt.edu.bd | test123 |
| redowan.alif | redowan.alif@bubt.edu.bd | password123 |

## How It Works

### Login Process:
1. User submits username/email and password
2. Python checks database for user
3. Password is verified using `check_password_hash()`
4. Session is created with user info
5. User is redirected to dashboard

### Registration Process:
1. User fills registration form
2. Python validates all inputs
3. Checks for duplicate username/email
4. Password is hashed using `generate_password_hash()`
5. New user is saved to database
6. User is redirected to login

### Password Security:
- Passwords are NEVER stored in plain text
- Uses Werkzeug's password hashing (bcrypt)
- Each password has unique salt
- Cannot be reversed or decrypted

## API Endpoints

### Login
- **POST** `/login`
  - Body: `username`, `password`, `rememberMe` (optional)
  - Returns: JSON with `success` and `message`

### Registration
- **POST** `/register`
  - Body: `username`, `email`, `password`, `confirmPassword`, `firstName`, `lastName`
  - Returns: JSON with `success` and `message`

### Logout
- **GET** `/logout`
  - Clears session and redirects to login

## Code Structure

### User Model
```python
class User(db.Model):
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### Login Route
- Handles both form submission and JSON requests
- Validates input
- Checks user in database
- Creates session
- Returns appropriate response

### Protected Routes
All routes use session check:
```python
if 'user_id' not in session:
    flash('Please login', 'warning')
    return redirect(url_for('login'))
```

## Security Features

1. **Password Hashing**: All passwords are hashed before storage
2. **Session Security**: Flask sessions with secret key
3. **Input Validation**: All inputs are validated
4. **SQL Injection Protection**: Using SQLAlchemy ORM
5. **CSRF Protection**: Can be added with Flask-WTF

## Testing

### Test Login:
```bash
# Using curl
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"
```

### Test Registration:
```bash
curl -X POST http://localhost:5000/register \
  -d "username=newuser&email=new@bubt.edu.bd&password=pass123&confirmPassword=pass123"
```

## Notes

- All authentication is done server-side (Python)
- No client-side password validation (security)
- Sessions expire after browser close (unless "Remember Me")
- Database is automatically initialized with default users

