"""
Script to update existing admin users to have is_admin=True
"""
from app import app, db, User

def update_admin_users():
    """Update admin users to have is_admin=True"""
    with app.app_context():
        # Update admin user
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.is_admin = True
            db.session.commit()
            print(f"[OK] Updated admin user: {admin_user.username}")
        else:
            print("[WARNING] Admin user not found!")
        
        # List all admin users
        admin_users = User.query.filter_by(is_admin=True).all()
        print(f"\nTotal admin users: {len(admin_users)}")
        for user in admin_users:
            print(f"  - {user.username} ({user.email})")

if __name__ == '__main__':
    print("=" * 50)
    print("Update Admin Users")
    print("=" * 50)
    update_admin_users()
    print("\nDone!")


