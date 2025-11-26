"""
Utility to view user information and manage passwords
Note: Passwords are hashed and cannot be viewed, but you can reset them
"""
from app import app, db, User
from werkzeug.security import check_password_hash

def view_all_users():
    """View all users with their information"""
    with app.app_context():
        users = User.query.all()
        print("\n" + "=" * 70)
        print("ALL USERS IN USERID TABLE")
        print("=" * 70)
        print(f"\nTotal users: {len(users)}\n")
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Password Hash: {user.password_hash[:50]}..." if len(user.password_hash) > 50 else f"  Password Hash: {user.password_hash}")
            print(f"  Created: {user.created_at}")
            print(f"  Remember Me: {user.remember_me}")
            print("-" * 70)
        
        print("\nNote: Passwords are hashed and cannot be viewed.")
        print("To reset a password, use: python reset_user_password.py reset <username> <new_password>")

def view_user(username):
    """View specific user information"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            print("\n" + "=" * 70)
            print(f"USER INFORMATION: {username}")
            print("=" * 70)
            print(f"\nID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Password Hash: {user.password_hash}")
            print(f"Password Hash Length: {len(user.password_hash)} characters")
            print(f"Created: {user.created_at}")
            print(f"Remember Me: {user.remember_me}")
            print("\n" + "=" * 70)
            print("Note: Password is hashed and cannot be decrypted.")
            print("To reset password, use:")
            print(f"  python reset_user_password.py reset {username} <new_password>")
        else:
            print(f"\n[ERROR] User '{username}' not found!")

def test_password(username, password):
    """Test if a password matches for a user"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                print(f"\n[OK] Password is CORRECT for user '{username}'")
                return True
            else:
                print(f"\n[ERROR] Password is INCORRECT for user '{username}'")
                return False
        else:
            print(f"\n[ERROR] User '{username}' not found!")
            return False

if __name__ == '__main__':
    import sys
    
    print("\n" + "=" * 70)
    print("USER INFORMATION VIEWER")
    print("=" * 70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python view_users.py list                          # List all users")
        print("  python view_users.py view <username>                 # View specific user")
        print("  python view_users.py test <username> <password>      # Test password")
        print("\nExample:")
        print("  python view_users.py list")
        print("  python view_users.py view redowan.alif")
        print("  python view_users.py test redowan.alif redwan1234")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        view_all_users()
    elif command == 'view':
        if len(sys.argv) < 3:
            print("Error: Username required")
            print("Usage: python view_users.py view <username>")
            sys.exit(1)
        username = sys.argv[2]
        view_user(username)
    elif command == 'test':
        if len(sys.argv) < 4:
            print("Error: Username and password required")
            print("Usage: python view_users.py test <username> <password>")
            sys.exit(1)
        username = sys.argv[2]
        password = sys.argv[3]
        test_password(username, password)
    else:
        print(f"Unknown command: {command}")
        print("Use 'list', 'view', or 'test'")


