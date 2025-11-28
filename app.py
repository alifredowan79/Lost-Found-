from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin_user(self):
        """Check if user is admin"""
        return self.is_admin or self.username == 'admin'


class Item(db.Model):
    """Lost and Found Item model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'lost' or 'found'
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(50), default='fas fa-question-circle')
    
    # Additional fields
    building = db.Column(db.String(100))
    floor = db.Column(db.String(50))
    color = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    value = db.Column(db.Float)
    phone = db.Column(db.String(20))
    student_id = db.Column(db.String(50))
    notes = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Invoice(db.Model):
    """Invoice model for found items"""
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue, cancelled
    
    # Client information
    client_name = db.Column(db.String(200), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_phone = db.Column(db.String(20))
    client_id = db.Column(db.String(50))
    
    # Item information
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_description = db.Column(db.Text)
    item_location = db.Column(db.String(200))
    item_date = db.Column(db.Date)
    
    # Fees
    processing_fee = db.Column(db.Float, default=5.00)
    storage_fee = db.Column(db.Float, default=2.00)
    late_fee = db.Column(db.Float, default=1.00)
    total_amount = db.Column(db.Float, nullable=False)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item', backref=db.backref('invoices', lazy=True))


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


# Utility Functions
def get_category_icon(category):
    """Get FontAwesome icon for category"""
    icon_map = {
        'electronics': 'fas fa-laptop',
        'jewelry': 'fas fa-gem',
        'clothing': 'fas fa-tshirt',
        'documents': 'fas fa-file-alt',
        'keys': 'fas fa-key',
        'books': 'fas fa-book',
        'bags': 'fas fa-briefcase',
        'watches': 'fas fa-clock',
        'other': 'fas fa-question-circle'
    }
    return icon_map.get(category, 'fas fa-question-circle')


def format_date(date_obj):
    """Format date for display"""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
    return date_obj.strftime('%b %d, %Y')


def generate_invoice_number():
    """Generate unique invoice number"""
    timestamp = int(datetime.now().timestamp() * 1000)
    random = db.session.query(Invoice).count() + 1
    return f'INV-{timestamp}-{random}'


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
            if request.is_json:
                return jsonify({'success': False, 'message': '; '.join(errors)}), 400
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful! You can now login.',
                    'redirect': url_for('login')
                })
            
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            error_msg = 'Registration failed. Please try again.'
            if request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 500
            flash(error_msg, 'error')
            return render_template('register.html')
    
    return render_template('register.html')


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
    
    # Get statistics
    total_items = Item.query.count()
    lost_items = Item.query.filter_by(status='lost').count()
    found_items = Item.query.filter_by(status='found').count()
    total_invoices = Invoice.query.count()
    
    # Get today's summary
    today = datetime.now().date()
    today_lost = Item.query.filter(
        Item.status == 'lost',
        db.func.date(Item.date) == today
    ).count()
    today_found = Item.query.filter(
        Item.status == 'found',
        db.func.date(Item.date) == today
    ).count()
    today_invoices = Invoice.query.filter(
        db.func.date(Invoice.date) == today
    ).count()
    
    # Get recent items
    recent_items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
    
    # Check if user is admin
    user = User.query.get(session.get('user_id'))
    is_admin = user.is_admin_user() if user else False
    
    return render_template('dashboard.html',
                         total_items=total_items,
                         lost_items=lost_items,
                         found_items=found_items,
                         total_invoices=total_invoices,
                         today_lost=today_lost,
                         today_found=today_found,
                         today_invoices=today_invoices,
                         recent_items=recent_items,
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
                    item_category = request.form.get('category', '').strip()
                    item_date_str = request.form.get('date-lost', '').strip()
                    item_location = request.form.get('location', '').strip()
                    item_description = request.form.get('description', '').strip()
                    item_contact = request.form.get('contact', '').strip()
                    item_phone = request.form.get('phone', '').strip()
                else:  # found
                    item_name = request.form.get('found-item-name', '').strip()
                    item_category = request.form.get('found-category', '').strip()
                    item_date_str = request.form.get('date-found', '').strip()
                    item_location = request.form.get('found-location', '').strip()
                    item_description = request.form.get('found-description', '').strip()
                    item_contact = request.form.get('found-contact', '').strip()
                    item_phone = request.form.get('found-phone', '').strip()
                
                # Validate required fields
                if not all([item_name, item_category, item_date_str, item_location, item_description, item_contact]):
                    flash('Please fill in all required fields', 'error')
                    return redirect(url_for('report'))
                
                # Parse date
                try:
                    item_date = datetime.strptime(item_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Invalid date format', 'error')
                    return redirect(url_for('report'))
                
                # Create new item
                new_item = Item(
                    name=item_name,
                    category=item_category,
                    status=form_type,
                    date=item_date,
                    location=item_location,
                    description=item_description,
                    contact=item_contact,
                    phone=item_phone if item_phone else None,
                    icon=get_category_icon(item_category)
                )
                
                db.session.add(new_item)
                db.session.commit()
                
                flash(f'{form_type.capitalize()} item reported successfully!', 'success')
                return redirect(url_for('report'))
            except Exception as e:
                app.logger.error(f'Error creating report: {str(e)}')
                import traceback
                app.logger.error(traceback.format_exc())
                flash(f'Error submitting report: {str(e)}', 'error')
                return redirect(url_for('report'))
        
        # Check if user is admin
        is_admin = require_admin()
        
        return render_template('report.html', is_admin=is_admin)
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
        
        # Build query
        query = Item.query
        
        if search_term:
            query = query.filter(
                db.or_(
                    Item.name.ilike(f'%{search_term}%'),
                    Item.description.ilike(f'%{search_term}%'),
                    Item.location.ilike(f'%{search_term}%')
                )
            )
        
        if category:
            query = query.filter(Item.category == category)
        
        if status:
            query = query.filter(Item.status == status)
        
        if date_from:
            query = query.filter(Item.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
        
        if date_to:
            query = query.filter(Item.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
        
        if location:
            query = query.filter(Item.location.ilike(f'%{location}%'))
        
        # Get sort parameter
        sort_by = request.args.get('sort', 'date-desc')
        if sort_by == 'date-desc':
            query = query.order_by(Item.date.desc())
        elif sort_by == 'date-asc':
            query = query.order_by(Item.date.asc())
        elif sort_by == 'name-asc':
            query = query.order_by(Item.name.asc())
        elif sort_by == 'name-desc':
            query = query.order_by(Item.name.desc())
        elif sort_by == 'category':
            query = query.order_by(Item.category.asc())
        elif sort_by == 'status':
            query = query.order_by(Item.status.asc())
        
        items = query.all()
        
        # Get user info for template
        user = User.query.get(session.get('user_id'))
        is_admin = user.is_admin_user() if user else False
        
        print(f"[DEBUG] Rendering search.html with {len(items)} items")
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
    """Create new item page"""
    if 'user_id' not in session:
        flash('Please login to create items', 'warning')
        return redirect(url_for('login'))
    
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
            if not all([item_name, item_category, item_date_str, item_location, item_description, item_contact]):
                flash('Please fill in all required fields', 'error')
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
            
            # Create new item (default status as 'found' for created items)
            new_item = Item(
                name=item_name,
                category=item_category,
                status='found',  # Default status for created items
                date=item_date,
                location=item_location,
                description=item_description,
                contact=item_contact,
                color=item_color if item_color else None,
                brand=item_brand if item_brand else None,
                value=item_value,
                icon=get_category_icon(item_category)
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
        
        print(f"[DEBUG] Rendering create-item.html for user: {session.get('username')}")
        result = render_template('create-item.html', 
                             username=session.get('username', 'User'),
                             is_admin=is_admin)
        print(f"[DEBUG] Template rendered successfully, length: {len(result)}")
        return result
    except Exception as e:
        import traceback
        error_msg = f'Error rendering create-item template: {str(e)}\n{traceback.format_exc()}'
        app.logger.error(error_msg)
        print(f"[ERROR] {error_msg}")
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    """Invoice generation page"""
    if 'user_id' not in session:
        flash('Please login to generate invoices', 'warning')
        return redirect(url_for('login'))
    
    try:
        if request.method == 'POST':
            # Create new invoice
            new_invoice = Invoice(
                invoice_number=generate_invoice_number(),
                date=datetime.strptime(request.form.get('invoice-date'), '%Y-%m-%d').date(),
                due_date=datetime.strptime(request.form.get('due-date'), '%Y-%m-%d').date(),
                status=request.form.get('invoice-status', 'pending'),
                client_name=request.form.get('client-name'),
                client_email=request.form.get('client-email'),
                client_phone=request.form.get('client-phone'),
                client_id=request.form.get('client-id'),
                item_id=int(request.form.get('invoice-item')),
                item_description=request.form.get('item-description'),
                item_location=request.form.get('item-location'),
                item_date=datetime.strptime(request.form.get('item-date'), '%Y-%m-%d').date() if request.form.get('item-date') else None,
                processing_fee=float(request.form.get('processing-fee', 5.00)),
                storage_fee=float(request.form.get('storage-fee', 2.00)),
                late_fee=float(request.form.get('late-fee', 1.00)),
                total_amount=float(request.form.get('total-amount')),
                notes=request.form.get('invoice-notes')
            )
            
            db.session.add(new_invoice)
            db.session.commit()
            
            flash('Invoice generated successfully!', 'success')
            return redirect(url_for('invoice'))
        
        # Get found items for dropdown
        found_items = Item.query.filter_by(status='found').all()
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        
        # Calculate statistics
        total_invoices = Invoice.query.count()
        total_revenue = db.session.query(db.func.sum(Invoice.total_amount)).scalar() or 0
        this_month = Invoice.query.filter(
            db.extract('month', Invoice.date) == datetime.now().month,
            db.extract('year', Invoice.date) == datetime.now().year
        ).count()
        
        return render_template('invoice.html',
                             found_items=found_items,
                             invoices=invoices,
                             total_invoices=total_invoices,
                             total_revenue=total_revenue,
                             this_month=this_month)
    except Exception as e:
        app.logger.error(f'Error in invoice route: {str(e)}')
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/about')
def about():
    """About page"""
    if 'user_id' not in session:
        flash('Please login to view this page', 'warning')
        return redirect(url_for('login'))
    try:
        return render_template('about.html')
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


@app.route('/admin/files')
def admin_files():
    """Admin-only page to view created files"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if not require_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # List of created utility files
        created_files = [
        {
            'name': 'reset_user_password.py',
            'description': 'Password reset utility - Reset user passwords',
            'usage': 'python reset_user_password.py reset <username> <password>',
            'category': 'Utility Script'
        },
        {
            'name': 'view_users.py',
            'description': 'User information viewer - View all users and test passwords',
            'usage': 'python view_users.py list',
            'category': 'Utility Script'
        }
        ]
        
        return render_template('admin_files.html', files=created_files, username=session.get('username', 'Admin'))
    except Exception as e:
        app.logger.error(f'Error in admin_files route: {str(e)}')
        flash('Error loading page. Please try again.', 'error')
        return redirect(url_for('dashboard'))


# API Routes
@app.route('/api/items', methods=['GET', 'POST'])
def api_items():
    """API endpoint for items"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'status': item.status,
            'date': item.date.isoformat(),
            'location': item.location,
            'description': item.description,
            'contact': item.contact,
            'icon': item.icon
        } for item in items])
    
    elif request.method == 'POST':
        data = request.json
        new_item = Item(
            name=data['name'],
            category=data['category'],
            status=data['status'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            location=data['location'],
            description=data['description'],
            contact=data['contact'],
            icon=get_category_icon(data['category'])
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'success': True, 'id': new_item.id}), 201


@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def api_item(item_id):
    """API endpoint for single item"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'status': item.status,
            'date': item.date.isoformat(),
            'location': item.location,
            'description': item.description,
            'contact': item.contact,
            'icon': item.icon
        })
    
    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.status = data.get('status', item.status)
        item.location = data.get('location', item.location)
        item.description = data.get('description', item.description)
        item.contact = data.get('contact', item.contact)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})


@app.route('/api/invoices', methods=['GET', 'POST'])
def api_invoices():
    """API endpoint for invoices"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        invoices = Invoice.query.all()
        return jsonify([{
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'date': invoice.date.isoformat(),
            'due_date': invoice.due_date.isoformat(),
            'status': invoice.status,
            'client_name': invoice.client_name,
            'client_email': invoice.client_email,
            'total_amount': invoice.total_amount
        } for invoice in invoices])
    
    elif request.method == 'POST':
        data = request.json
        new_invoice = Invoice(
            invoice_number=generate_invoice_number(),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
            status=data.get('status', 'pending'),
            client_name=data['client_name'],
            client_email=data['client_email'],
            item_id=data['item_id'],
            total_amount=data['total_amount']
        )
        db.session.add(new_invoice)
        db.session.commit()
        return jsonify({'success': True, 'id': new_invoice.id}), 201


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    total_items = Item.query.count()
    lost_items = Item.query.filter_by(status='lost').count()
    found_items = Item.query.filter_by(status='found').count()
    total_invoices = Invoice.query.count()
    
    return jsonify({
        'total_items': total_items,
        'lost_items': lost_items,
        'found_items': found_items,
        'total_invoices': total_invoices
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
        
        # Add sample items if database is empty
        if Item.query.count() == 0:
            sample_items = [
                Item(
                    name="iPhone 13 Pro",
                    category="electronics",
                    status="lost",
                    date=datetime(2024, 1, 15).date(),
                    location="Main Library, 2nd Floor",
                    description="Black iPhone 13 Pro with blue case. Has a small scratch on the back.",
                    contact="john.doe@bubt.edu.bd",
                    icon="fas fa-mobile-alt"
                ),
                Item(
                    name="Gold Necklace",
                    category="jewelry",
                    status="found",
                    date=datetime(2024, 1, 14).date(),
                    location="Student Center, Cafeteria",
                    description="Delicate gold chain necklace with a small pendant.",
                    contact="security@bubt.edu.bd",
                    icon="fas fa-gem"
                ),
                Item(
                    name="Car Keys",
                    category="keys",
                    status="lost",
                    date=datetime(2024, 1, 13).date(),
                    location="Parking Lot A",
                    description="Toyota car keys with a black keychain.",
                    contact="jane.smith@bubt.edu.bd",
                    icon="fas fa-key"
                ),
            ]
            
            for item in sample_items:
                db.session.add(item)
            
            db.session.commit()
            print("Sample items created successfully!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

