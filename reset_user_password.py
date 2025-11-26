"""
Utility script to check and reset user password in userid table
"""
from app import app, db, User
from werkzeug.security import generate_password_hash, check_password_hash

def check_user(username):
    """Check if user exists and verify password"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"\n[OK] User found: {username}")
            print(f"  Email: {user.email}")
            print(f"  ID: {user.id}")
            print(f"  Password hash exists: {bool(user.password_hash)}")
            return user
        else:
            print(f"\n[ERROR] User '{username}' not found in userid table")
            return None

def reset_password(username, new_password):
    """Reset user password"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            print(f"\n[OK] Password reset successfully for {username}")
            return True
        else:
            print(f"\n[ERROR] User '{username}' not found")
            return False

def list_all_users():
    """List all users in userid table"""
    with app.app_context():
        users = User.query.all()
        print(f"\n=== All Users in userid table ===")
        print(f"Total users: {len(users)}\n")
        for user in users:
            print(f"  ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Created: {user.created_at}")
            print()

if __name__ == '__main__':
    import sys
    
    print("=" * 50)
    print("User Password Management Tool")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python reset_user_password.py list                    # List all users")
        print("  python reset_user_password.py check <username>       # Check user")
        print("  python reset_user_password.py reset <username> <password>  # Reset password")
        print("\nExample:")
        print("  python reset_user_password.py check redowan.alif")
        print("  python reset_user_password.py reset redowan.alif newpassword123")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_all_users()
    elif command == 'check':
        if len(sys.argv) < 3:
            print("Error: Username required")
            sys.exit(1)
        username = sys.argv[2]
        check_user(username)
    elif command == 'reset':
        if len(sys.argv) < 4:
            print("Error: Username and password required")
            print("Usage: python reset_user_password.py reset <username> <password>")
            sys.exit(1)
        username = sys.argv[2]
        new_password = sys.argv[3]
        reset_password(username, new_password)
    else:
        print(f"Unknown command: {command}")

