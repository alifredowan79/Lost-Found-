from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
# Get the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path=env_path)


def env_bool(var_name, default=False):
    """Return True if environment variable is truthy."""
    value = os.getenv(var_name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Database configuration
# Priority: Explicit SQLite flag > DATABASE_URL > PostgreSQL env vars > SQLite fallback
database_url = os.getenv('DATABASE_URL')
force_sqlite = env_bool('USE_SQLITE')
use_sqlite = False

if not force_sqlite and database_url:
    # Database URL provided explicitly (supports PostgreSQL, etc.)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("Using database from DATABASE_URL")
elif not force_sqlite and os.getenv('DB_HOST'):
    # PostgreSQL from individual environment variables
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'lost_found')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    print(f"Connected to PostgreSQL database: {db_name} on {db_host}:{db_port}")
else:
    # SQLite configuration (explicit or fallback)
    sqlite_path = os.getenv('SQLITE_DB_PATH', os.path.join(basedir, 'lost_found.db'))
    if sqlite_path.startswith('sqlite:'):
        sqlite_uri = sqlite_path
    else:
        sqlite_uri = f"sqlite:///{sqlite_path}"
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
    use_sqlite = True
    if force_sqlite:
        print(f"Using SQLite database as requested via USE_SQLITE (path: {sqlite_path}).")
    else:
        print("WARNING: PostgreSQL not configured. Using SQLite database.")
        print("TIP: To use PostgreSQL, create a .env file with DB_HOST, DB_PORT, DB_NAME, DB_USER, and DB_PASSWORD")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure engine options based on database type
if use_sqlite:
    # SQLite-specific configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'check_same_thread': False  # Allow SQLite to work with Flask's threading
        }
    }
else:
    # PostgreSQL-specific configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'connect_timeout': 10
        }
    }

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'userid'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    remember_me = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # Store password in plain text (normal format)
        self.password_hash = password

    def check_password(self, password):
        # Compare plain text passwords
        return self.password_hash == password
    
    def is_admin_user(self):
        """Check if user is admin"""
        return self.is_admin or self.username == 'admin'


class Item(db.Model):
    """Lost and Found Item model - Simplified with name as primary key"""
    # Primary key
    name = db.Column(db.String(200), primary_key=True)  # Item Name *
    
    # Required fields
    category = db.Column(db.String(50), nullable=False)  # Category *
    date = db.Column(db.Date, nullable=False)  # Date *
    description = db.Column(db.Text, nullable=False)  # Description *
    
    # Optional fields
    color = db.Column(db.String(50), nullable=True)  # Color (optional)
    brand = db.Column(db.String(100), nullable=True)  # Brand/Model (optional)
    value = db.Column(db.Float, nullable=True)  # Estimated Value (optional)


class LostFoundItem(db.Model):
    """Lost and Found Items reported through report screen"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Item information - name is foreign key to Item table (composite key)
    name = db.Column(db.String(200), db.ForeignKey('item.name'), nullable=False)  # Item Name * (Foreign Key)
    category = db.Column(db.String(50), nullable=False)  # Category *
    date = db.Column(db.Date, nullable=False)  # Date Lost/Found *
    location = db.Column(db.String(200), nullable=False)  # Location Lost/Found *
    description = db.Column(db.Text, nullable=False)  # Description *
    
    # Contact information
    contact = db.Column(db.String(120), nullable=False)  # Contact Email *
    phone = db.Column(db.String(20), nullable=True)  # Phone Number (optional)
    student_id = db.Column(db.String(50), nullable=True)  # Student ID (optional)
    program = db.Column(db.String(50), nullable=True)  # Program (BSC, BBA, MBA, MCS, etc.) (optional)
    department = db.Column(db.String(100), nullable=True)  # Department (optional)
    
    # Status
    status = db.Column(db.String(20), nullable=False)  # 'lost' or 'found'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to Item table
    item = db.relationship('Item', backref=db.backref('lost_found_items', lazy=True))


# Authentication Helper
def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():
    """Welcome page - landing page before login"""
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with Python authentication"""
    # If already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('rememberMe')
        # Check if this is an AJAX/JSON request
        is_json = (request.headers.get('Content-Type') == 'application/json' or 
                  request.is_json or 
                  request.headers.get('X-Requested-With') == 'XMLHttpRequest')
        
        # Validate input
        if not username_or_email or not password:
            error_msg = 'Username/Email and password are required'
            if is_json:
                return jsonify({'success': False, 'message': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('login.html')
        
        # Try to find user by username or email from userid table
        # Note: User.query automatically uses the 'userid' table (defined in __tablename__)
        try:
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            # Debug: Check if user exists
            if not user:
                error_msg = f'User "{username_or_email}" not found in database'
                if is_json:
                    return jsonify({'success': False, 'message': 'Invalid username/email or password'}), 401
                flash('Invalid username/email or password', 'error')
                return render_template('login.html')
            
            # Authenticate user - password check uses userid table
            if user.check_password(password):
                # Login successful
                session['user_id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                
                if remember_me:
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(days=30)
                
                if is_json:
                    return jsonify({
                        'success': True, 
                        'message': 'Login successful',
                        'redirect': url_for('dashboard')
                    })
                
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Password mismatch
                error_msg = 'Invalid password'
                if is_json:
                    return jsonify({'success': False, 'message': 'Invalid username/email or password'}), 401
                flash('Invalid username/email or password', 'error')
                return render_template('login.html')
                
        except Exception as e:
            # Log the error for debugging
            import traceback
            app.logger.error(f'Login error: {str(e)}')
            app.logger.error(f'Traceback: {traceback.format_exc()}')
            print(f'[ERROR] Login exception: {str(e)}')
            print(f'[ERROR] Traceback: {traceback.format_exc()}')
            error_msg = 'An error occurred during login. Please try again.'
            if is_json:
                return jsonify({'success': False, 'message': error_msg}), 500
            flash(error_msg, 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        
        app.logger.info(f'Registration attempt - Username: {username}, Email: {email}')
        
        # Validate input
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if not email or '@' not in email:
            errors.append('Valid email address is required')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
            if errors:
                error_message = '; '.join(errors)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                    return jsonify({'success': False, 'message': error_message}), 400
                for error in errors:
                    flash(error, 'error')
                # Check if user is admin for template
                user = None
                is_admin = False
                if 'user_id' in session:
                    user = User.query.get(session.get('user_id'))
                    is_admin = user.is_admin_user() if user else False
                return render_template('register.html', is_admin=is_admin)
        
        # Create new user
        try:
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            app.logger.info(f'User registered successfully - Username: {username}, Email: {email}')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful! You can now login.',
                    'redirect': url_for('login')
                })
            
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Registration error: {str(e)}')
            error_msg = 'Registration failed. Please try again.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 500
            flash(error_msg, 'error')
            # Check if user is admin for template
            user = None
            is_admin = False
            if 'user_id' in session:
                user = User.query.get(session.get('user_id'))
                is_admin = user.is_admin_user() if user else False
            return render_template('register.html', is_admin=is_admin)
    
    # Check if user is admin for template
    user = None
    is_admin = False
    if 'user_id' in session:
        user = User.query.get(session.get('user_id'))
        is_admin = user.is_admin_user() if user else False
    
    return render_template('register.html', is_admin=is_admin)


@app.route('/logout')
def logout():
    """Logout user"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        flash('Please login to access the dashboard', 'warning')
        return redirect(url_for('login'))
    
    # Get real-time statistics from database
    total_items = Item.query.count()
    total_lost_found = LostFoundItem.query.count()
    
    # Get lost and found counts from LostFoundItem table
    lost_items_count = LostFoundItem.query.filter_by(status='lost').count()
    found_items_count = LostFoundItem.query.filter_by(status='found').count()
    
    # Get today's summary
    today = datetime.now().date()
    today_items = Item.query.filter(
        db.func.date(Item.date) == today
    ).count()
    today_lost = LostFoundItem.query.filter(
        db.func.date(LostFoundItem.date) == today,
        LostFoundItem.status == 'lost'
    ).count()
    today_found = LostFoundItem.query.filter(
        db.func.date(LostFoundItem.date) == today,
        LostFoundItem.status == 'found'
    ).count()
    
    # Get recent lost/found items (from LostFoundItem table)
    recent_lost_found = LostFoundItem.query.order_by(
        LostFoundItem.created_at.desc()
    ).limit(10).all()
    
    # Get recent items (from Item table)
    recent_items = Item.query.order_by(Item.date.desc()).limit(10).all()
    
    # Get weekly statistics (last 7 days)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    weekly_lost = LostFoundItem.query.filter(
        LostFoundItem.date >= seven_days_ago,
        LostFoundItem.status == 'lost'
    ).count()
    weekly_found = LostFoundItem.query.filter(
        LostFoundItem.date >= seven_days_ago,
        LostFoundItem.status == 'found'
    ).count()
    
    # Check if user is admin
    user = User.query.get(session.get('user_id'))
    is_admin = user.is_admin_user() if user else False
    
    return render_template('dashboard.html',
                         total_items=total_items,
                         total_lost_found=total_lost_found,
                         lost_items=lost_items_count,
                         found_items=found_items_count,
                         today_items=today_items,
                         today_lost=today_lost,
                         today_found=today_found,
                         weekly_lost=weekly_lost,
                         weekly_found=weekly_found,
                         recent_items=recent_items,
                         recent_lost_found=recent_lost_found,
                         username=session.get('username', 'User'),
                         is_admin=is_admin)


@app.route('/report', methods=['GET', 'POST'])
def report():
    """Report lost/found items page"""
    if 'user_id' not in session:
        flash('Please login to report items', 'warning')
        return redirect(url_for('login'))
    
    try:
        if request.method == 'POST':
            form_type = request.form.get('form_type', 'lost')
            
            try:
                # Get form data based on form type
                if form_type == 'lost':
                    item_name = request.form.get('item-name', '').strip()
                    item_date_str = request.form.get('date-lost', '').strip()
                    item_location = request.form.get('location', '').strip()
                    item_description = request.form.get('description', '').strip()
                    item_contact = request.form.get('contact', '').strip()
                    item_phone = request.form.get('phone', '').strip()
                    item_student_id = request.form.get('student-id', '').strip()
                    item_program = request.form.get('program', '').strip()
                    item_department = request.form.get('department', '').strip()
                else:  # found
                    item_name = request.form.get('found-item-name', '').strip()
                    item_date_str = request.form.get('date-found', '').strip()
                    item_location = request.form.get('found-location', '').strip()
                    item_description = request.form.get('found-description', '').strip()
                    item_contact = request.form.get('found-contact', '').strip()
                    item_phone = request.form.get('found-phone', '').strip()
                    item_student_id = request.form.get('found-student-id', '').strip()
                    item_program = request.form.get('found-program', '').strip()
                    item_department = request.form.get('found-department', '').strip()
                
                # Validate required fields
                if not all([item_name, item_date_str, item_location, item_description, item_contact]):
                    flash('Please fill in all required fields', 'error')
                    return redirect(url_for('report'))
                
                # Check if item exists in Item table (name must exist as foreign key)
                existing_item = Item.query.filter_by(name=item_name).first()
                if not existing_item:
                    flash(f'Item "{item_name}" does not exist in the system. Please create the item first using "Create Item" page.', 'error')
                    return redirect(url_for('report'))
                
                # Get category from the existing item
                item_category = existing_item.category
                
                # Parse date
                try:
                    item_date = datetime.strptime(item_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Invalid date format', 'error')
                    return redirect(url_for('report'))
                
                # Create new lost/found item in LostFoundItem table
                # name is foreign key referencing Item.name
                new_lost_found_item = LostFoundItem(
                    name=item_name,  # Foreign key to Item.name
                    category=item_category,  # Get from Item table
                    date=item_date,
                    location=item_location,
                    description=item_description,
                    contact=item_contact,
                    phone=item_phone if item_phone else None,
                    student_id=item_student_id if item_student_id else None,
                    program=item_program if item_program else None,
                    department=item_department if item_department else None,
                    status=form_type  # 'lost' or 'found'
                )
                
                db.session.add(new_lost_found_item)
                db.session.commit()
                
                flash(f'{form_type.capitalize()} item reported successfully!', 'success')
                return redirect(url_for('report'))
            except Exception as e:
                app.logger.error(f'Error creating report: {str(e)}')
                import traceback
                app.logger.error(traceback.format_exc())
                flash(f'Error submitting report: {str(e)}', 'error')
                return redirect(url_for('report'))
        
        # Get all items from Item table for dropdown selection
        all_items = Item.query.order_by(Item.name.asc()).all()
        
        # Get all lost and found items for display
        lost_items = LostFoundItem.query.filter_by(status='lost').order_by(LostFoundItem.date.desc()).all()
        found_items = LostFoundItem.query.filter_by(status='found').order_by(LostFoundItem.date.desc()).all()
        
        # Check if user is admin
        is_admin = require_admin()
        
        return render_template('report.html', 
                             is_admin=is_admin,
                             all_items=all_items,
                             lost_items=lost_items,
                             found_items=found_items)
    except Exception as e:
        app.logger.error(f'Error in report route: {str(e)}')
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/search')
def search():
    """Search items page"""
    if 'user_id' not in session:
        flash('Please login to search items', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Get filter parameters
        search_term = request.args.get('q', '').lower()
        category = request.args.get('category', '')
        status = request.args.get('status', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        location = request.args.get('location', '').lower()
        
        # Build query for LostFoundItem table (shows lost/found items with status)
        query = LostFoundItem.query
        
        if search_term:
            query = query.filter(
                db.or_(
                    LostFoundItem.name.ilike(f'%{search_term}%'),
                    LostFoundItem.description.ilike(f'%{search_term}%'),
                    LostFoundItem.location.ilike(f'%{search_term}%')
                )
            )
        
        if category:
            query = query.filter(LostFoundItem.category == category)
        
        if status:
            query = query.filter(LostFoundItem.status == status)
        
        if date_from:
            query = query.filter(LostFoundItem.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
        
        if date_to:
            query = query.filter(LostFoundItem.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
        
        if location:
            query = query.filter(LostFoundItem.location.ilike(f'%{location}%'))
        
        # Get sort parameter
        sort_by = request.args.get('sort', 'date-desc')
        if sort_by == 'date-desc':
            query = query.order_by(LostFoundItem.date.desc())
        elif sort_by == 'date-asc':
            query = query.order_by(LostFoundItem.date.asc())
        elif sort_by == 'name-asc':
            query = query.order_by(LostFoundItem.name.asc())
        elif sort_by == 'name-desc':
            query = query.order_by(LostFoundItem.name.desc())
        elif sort_by == 'category':
            query = query.order_by(LostFoundItem.category.asc())
        elif sort_by == 'status':
            query = query.order_by(LostFoundItem.status.asc())
        
        items = query.all()
        
        # Get user info for template
        user = User.query.get(session.get('user_id'))
        is_admin = user.is_admin_user() if user else False
        
        print(f"[DEBUG] Rendering search.html with {len(items)} lost/found items")
        result = render_template('search.html', 
                             items=items, 
                             search_term=search_term,
                             username=session.get('username', 'User'),
                             is_admin=is_admin)
        print(f"[DEBUG] Template rendered successfully, length: {len(result)}")
        return result
    except Exception as e:
        import traceback
        error_msg = f'Error in search route: {str(e)}\n{traceback.format_exc()}'
        app.logger.error(error_msg)
        print(f"[ERROR] {error_msg}")
        flash('Error loading search page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/create-item', methods=['GET', 'POST'])
def create_item():
    """Create new item page - Admin only"""
    if 'user_id' not in session:
        flash('Please login to create items', 'warning')
        return redirect(url_for('login'))
    
    # Check if user is admin
    user = User.query.get(session.get('user_id'))
    if not user or not user.is_admin_user():
        flash('Access denied. Only admin users can create items.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            # Get form data
            item_name = request.form.get('item-name', '').strip()
            item_category = request.form.get('item-category', '').strip()
            item_date_str = request.form.get('item-date', '').strip()
            item_location = request.form.get('item-location', '').strip()
            item_description = request.form.get('item-description', '').strip()
            item_color = request.form.get('item-color', '').strip()
            item_brand = request.form.get('item-brand', '').strip()
            item_value_str = request.form.get('item-value', '').strip()
            
            # Get user's email from session for contact
            item_contact = session.get('email', '')
            
            # Validate required fields
            if not all([item_name, item_category, item_date_str, item_description]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('create_item'))
            
            # Check if item with same name already exists
            existing_item = Item.query.filter_by(name=item_name).first()
            if existing_item:
                flash('An item with this name already exists. Please use a different name.', 'error')
                return redirect(url_for('create_item'))
            
            # Parse date
            try:
                item_date = datetime.strptime(item_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('create_item'))
            
            # Parse value
            item_value = None
            if item_value_str:
                try:
                    item_value = float(item_value_str)
                except ValueError:
                    item_value = None
            
            # Create new item
            new_item = Item(
                name=item_name,
                category=item_category,
                date=item_date,
                description=item_description,
                color=item_color if item_color else None,
                brand=item_brand if item_brand else None,
                value=item_value
            )
            
            db.session.add(new_item)
            db.session.commit()
            
            flash('Item created successfully!', 'success')
            return redirect(url_for('create_item'))
        except Exception as e:
            app.logger.error(f'Error creating item: {str(e)}')
            import traceback
            app.logger.error(traceback.format_exc())
            flash(f'Error creating item: {str(e)}', 'error')
            return redirect(url_for('create_item'))
    
    try:
        # Get user info for template
        user = User.query.get(session.get('user_id'))
        is_admin = user.is_admin_user() if user else False
        
        # Get all items from database - show minimum 10 most recent items
        # Order by date descending for most recent first
        available_items = Item.query.order_by(Item.date.desc()).limit(10).all()
        
        # Debug: Print item count and first item details to confirm database data
        print(f"[DEBUG] Available items from DATABASE: {len(available_items)} items found")
        if available_items:
            print(f"[DEBUG] First item from DB: {available_items[0].name} - {available_items[0].category} - Date: {available_items[0].date}")
        else:
            print(f"[DEBUG] No items found in database")
        
        print(f"[DEBUG] Rendering create-item.html for user: {session.get('username')}")
        result = render_template('create-item.html', 
                             username=session.get('username', 'User'),
                             is_admin=is_admin,
                             available_items=available_items)
        print(f"[DEBUG] Template rendered successfully, length: {len(result)}")
        return result
    except Exception as e:
        import traceback
        error_msg = f'Error rendering create-item template: {str(e)}\n{traceback.format_exc()}'
        app.logger.error(error_msg)
        print(f"[ERROR] {error_msg}")
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/about')
def about():
    """About page with real-time statistics"""
    if 'user_id' not in session:
        flash('Please login to view this page', 'warning')
        return redirect(url_for('login'))
    try:
        # Get real-time statistics
        total_items = Item.query.count()
        total_lost_found_items = LostFoundItem.query.count()
        total_users = User.query.count()
        
        # Get lost and found counts
        lost_items_count = LostFoundItem.query.filter_by(status='lost').count()
        found_items_count = LostFoundItem.query.filter_by(status='found').count()
        
        # Get today's activity
        today = datetime.now().date()
        today_items = Item.query.filter(
            db.func.date(Item.date) == today
        ).count()
        today_lost_found = LostFoundItem.query.filter(
            db.func.date(LostFoundItem.date) == today
        ).count()
        
        # Get recent items (last 7 days)
        seven_days_ago = datetime.now().date() - timedelta(days=7)
        recent_items_count = LostFoundItem.query.filter(
            LostFoundItem.date >= seven_days_ago
        ).count()
        
        # Calculate success rate (found items / total lost+found items)
        success_rate = 0
        if total_lost_found_items > 0:
            success_rate = round((found_items_count / total_lost_found_items) * 100, 1)
        
        # Get most active categories
        category_counts = db.session.query(
            LostFoundItem.category,
            db.func.count(LostFoundItem.id).label('count')
        ).group_by(LostFoundItem.category).order_by(db.func.count(LostFoundItem.id).desc()).limit(5).all()
        
        # Get recent activity (last 5 items)
        recent_activity = LostFoundItem.query.order_by(
            LostFoundItem.created_at.desc()
        ).limit(5).all()
        
        # Get user info for template
        user = User.query.get(session.get('user_id'))
        is_admin = user.is_admin_user() if user else False
        
        return render_template('about.html',
                             total_items=total_items,
                             total_lost_found_items=total_lost_found_items,
                             total_users=total_users,
                             lost_items_count=lost_items_count,
                             found_items_count=found_items_count,
                             today_items=today_items,
                             today_lost_found=today_lost_found,
                             recent_items_count=recent_items_count,
                             success_rate=success_rate,
                             category_counts=category_counts,
                             recent_activity=recent_activity,
                             is_admin=is_admin)
    except Exception as e:
        app.logger.error(f'Error rendering about template: {str(e)}')
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


def require_admin():
    """Check if current user is admin"""
    if 'user_id' not in session:
        return False
    user = User.query.get(session['user_id'])
    if not user:
        return False
    return user.is_admin_user()


@app.route('/admin/files', methods=['GET', 'POST'])
def admin_files():
    """Admin-only page to view all users and manage them"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if not require_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Handle password reset
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'reset_password':
                user_id = int(request.form.get('user_id'))
                new_password = request.form.get('new_password', '').strip()
                
                if not new_password:
                    flash('Password cannot be empty', 'error')
                    return redirect(url_for('admin_files'))
                
                user = User.query.get(user_id)
                if user:
                    user.set_password(new_password)
                    db.session.commit()
                    flash(f'Password reset successfully for user: {user.username}', 'success')
                else:
                    flash('User not found', 'error')
                return redirect(url_for('admin_files'))
        
        # Get all users from database
        all_users = User.query.order_by(User.created_at.desc()).all()
        
        # Get user info for template
        current_user = User.query.get(session.get('user_id'))
        is_admin = current_user.is_admin_user() if current_user else False
        
        return render_template('admin_files.html', 
                             users=all_users,
                             username=session.get('username', 'Admin'),
                             is_admin=is_admin)
    except Exception as e:
        app.logger.error(f'Error in admin_files route: {str(e)}')
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


# API Routes
@app.route('/api/search', methods=['GET'])
def api_search():
    """API endpoint for searching lost/found items"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get filter parameters
    search_term = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    location = request.args.get('location', '').strip()
    
    # Build query for LostFoundItem table
    query = LostFoundItem.query
    
    if search_term:
        query = query.filter(
            db.or_(
                LostFoundItem.name.ilike(f'%{search_term}%'),
                LostFoundItem.description.ilike(f'%{search_term}%'),
                LostFoundItem.location.ilike(f'%{search_term}%')
            )
        )
    
    if category:
        query = query.filter(LostFoundItem.category == category)
    
    if status:
        query = query.filter(LostFoundItem.status == status)
    
    if date_from:
        query = query.filter(LostFoundItem.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    
    if date_to:
        query = query.filter(LostFoundItem.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    if location:
        query = query.filter(LostFoundItem.location.ilike(f'%{location}%'))
    
    items = query.order_by(LostFoundItem.date.desc()).all()
    
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'status': item.status,
        'date': item.date.isoformat(),
        'location': item.location,
        'description': item.description,
        'contact': item.contact,
        'phone': item.phone,
        'student_id': item.student_id,
        'program': item.program,
        'department': item.department
    } for item in items])

@app.route('/api/items', methods=['GET', 'POST'])
def api_items():
    """API endpoint for items"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{
            'name': item.name,
            'category': item.category,
            'date': item.date.isoformat(),
            'description': item.description,
            'color': item.color,
            'brand': item.brand,
            'value': item.value
        } for item in items])
    
    elif request.method == 'POST':
        data = request.json
        new_item = Item(
            name=data['name'],
            category=data['category'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            description=data['description'],
            color=data.get('color'),
            brand=data.get('brand'),
            value=data.get('value')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'success': True, 'name': new_item.name}), 201


@app.route('/api/items/<item_name>', methods=['GET', 'PUT', 'DELETE'])
def api_item(item_name):
    """API endpoint for single item (using name as primary key)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    item = Item.query.get_or_404(item_name)
    
    if request.method == 'GET':
        return jsonify({
            'name': item.name,
            'category': item.category,
            'date': item.date.isoformat(),
            'description': item.description,
            'color': item.color,
            'brand': item.brand,
            'value': item.value
        })
    
    elif request.method == 'PUT':
        data = request.json
        item.category = data.get('category', item.category)
        item.date = datetime.strptime(data.get('date', item.date.isoformat()), '%Y-%m-%d').date() if data.get('date') else item.date
        item.description = data.get('description', item.description)
        item.color = data.get('color', item.color)
        item.brand = data.get('brand', item.brand)
        item.value = data.get('value', item.value)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    total_items = Item.query.count()
    
    return jsonify({
        'total_items': total_items,
        'lost_items': 0,  # Status field removed
        'found_items': 0  # Status field removed
    })


# Initialize database
def init_db():
    """Create database tables and initialize with default data"""
    with app.app_context():
        db.create_all()
        
        # Create default users if they don't exist
        if User.query.count() == 0:
            default_users = [
                {
                    'username': 'admin',
                    'email': 'admin@bubt.edu.bd',
                    'password': 'admin123',
                    'is_admin': True
                },
                {
                    'username': 'user',
                    'email': 'user@bubt.edu.bd',
                    'password': 'user123'
                },
                {
                    'username': 'test',
                    'email': 'test@bubt.edu.bd',
                    'password': 'test123'
                },
                {
                    'username': 'redowan.alif',
                    'email': 'redowan.alif@bubt.edu.bd',
                    'password': 'password123'
                }
            ]
            
            for user_data in default_users:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    is_admin=user_data.get('is_admin', False)
                )
                user.set_password(user_data['password'])
                db.session.add(user)
            
            db.session.commit()
            print("Default users created successfully!")
        
        # Sample items creation removed - items will be created manually through the form


if __name__ == '__main__':
    init_db()
    # Use PORT environment variable if available (for production)
    port = int(os.environ.get('PORT', 5000))
    # Only enable debug in development
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

