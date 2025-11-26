"""
Script to add is_admin column to userid table
"""
from app import app, db
import sqlalchemy

def add_admin_column():
    """Add is_admin column to userid table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if column exists
            inspector = sqlalchemy.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('userid')]
            
            if 'is_admin' not in columns:
                print("Adding is_admin column to userid table...")
                # Add the column
                db.engine.execute(sqlalchemy.text(
                    "ALTER TABLE userid ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"
                ))
                print("[OK] Column added successfully!")
                
                # Update admin user
                db.engine.execute(sqlalchemy.text(
                    "UPDATE userid SET is_admin = TRUE WHERE username = 'admin'"
                ))
                print("[OK] Admin user updated!")
            else:
                print("[INFO] Column is_admin already exists")
                # Still update admin user
                db.engine.execute(sqlalchemy.text(
                    "UPDATE userid SET is_admin = TRUE WHERE username = 'admin'"
                ))
                print("[OK] Admin user updated!")
                
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            # Try alternative method
            try:
                with db.engine.connect() as conn:
                    conn.execute(sqlalchemy.text(
                        "ALTER TABLE userid ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE"
                    ))
                    conn.execute(sqlalchemy.text(
                        "UPDATE userid SET is_admin = TRUE WHERE username = 'admin'"
                    ))
                    conn.commit()
                    print("[OK] Column added and admin updated!")
            except Exception as e2:
                print(f"[ERROR] Alternative method also failed: {str(e2)}")
                print("\nPlease run this SQL manually in pgAdmin:")
                print("ALTER TABLE userid ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;")
                print("UPDATE userid SET is_admin = TRUE WHERE username = 'admin';")

if __name__ == '__main__':
    print("=" * 50)
    print("Add is_admin Column to userid Table")
    print("=" * 50)
    add_admin_column()
    print("\nDone!")


