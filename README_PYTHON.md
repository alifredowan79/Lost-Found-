# BUBT Lost and Found System - Python/Flask Version

This is the Python Flask backend version of the BUBT Lost and Found System. The JavaScript frontend has been converted to a Python Flask web application with SQLite database.

## Features

- **User Authentication**: Login system with session management
- **Item Management**: Create, view, search, and manage lost/found items
- **Dashboard**: Comprehensive dashboard with statistics and overview
- **Invoice Generation**: Generate invoices for found items
- **Search & Filter**: Advanced search functionality with multiple filters
- **RESTful API**: API endpoints for programmatic access

## Technology Stack

- **Backend**: Python 3.7+
- **Web Framework**: Flask 2.3.3
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML, CSS, JavaScript (with Jinja2 templates)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd Lost-Found-Prototype-main
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   The database will be automatically created when you run the application for the first time.

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

The application includes demo credentials:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`
- Username: `test@bubt.edu.bd`, Password: `test123`
- Username: `redowan.alif`, Password: `password123`

## Project Structure

```
Lost-Found-Prototype-main/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── lost_found.db         # SQLite database (created automatically)
├── templates/            # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── report.html
│   ├── search.html
│   ├── create-item.html
│   ├── invoice.html
│   └── about.html
├── static/              # Static files
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
└── README_PYTHON.md    # This file
```

## API Endpoints

### Items API
- `GET /api/items` - Get all items
- `POST /api/items` - Create new item
- `GET /api/items/<id>` - Get specific item
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item

### Invoices API
- `GET /api/invoices` - Get all invoices
- `POST /api/invoices` - Create new invoice

### Statistics API
- `GET /api/stats` - Get dashboard statistics

## Database Models

### User
- id, username, email, password_hash, remember_me, created_at

### Item
- id, name, category, status, date, location, description, contact, icon
- Additional fields: building, floor, color, brand, value, phone, student_id, notes, priority

### Invoice
- id, invoice_number, date, due_date, status
- Client info: client_name, client_email, client_phone, client_id
- Item info: item_id, item_description, item_location, item_date
- Fees: processing_fee, storage_fee, late_fee, total_amount

## Key Differences from JavaScript Version

1. **Data Storage**: Uses SQLite database instead of localStorage
2. **Server-Side Processing**: Business logic moved to Python backend
3. **Session Management**: Uses Flask sessions instead of localStorage
4. **Templates**: HTML converted to Jinja2 templates
5. **API**: RESTful API endpoints for data operations

## Development

### Running in Development Mode

```bash
python app.py
```

The application runs in debug mode by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar

### Database Management

The database is automatically created on first run. To reset the database:

1. Delete `lost_found.db`
2. Restart the application

## Production Deployment

For production deployment:

1. Change `SECRET_KEY` in `app.py` to a secure random value
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (e.g., Gunicorn)
4. Configure a reverse proxy (e.g., Nginx)
5. Use a production database (PostgreSQL, MySQL) instead of SQLite

## Troubleshooting

### Database Issues
- If you get database errors, delete `lost_found.db` and restart
- Ensure SQLite is installed on your system

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

## License

This project is for educational purposes.

## Support

For issues or questions, please refer to the original project documentation or contact the development team.

