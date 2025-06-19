"""
Initialize the admin account with hardcoded credentials
"""
from app import create_app, db
from app.models.user import User, ROLE_ADMIN
from werkzeug.security import generate_password_hash

# Hardcoded admin credentials
ADMIN_EMAIL = 'admin123@gmail.com'
ADMIN_PASSWORD = 'admin123'
ADMIN_NAME = 'Administrator'
ADMIN_COMPANY = 'Resume Screener'

def init_admin():
    """Create or update the admin account with hardcoded credentials"""
    app = create_app()
    
    with app.app_context():
        # Check if admin account already exists
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        
        if admin:
            print(f"Admin account already exists: {ADMIN_EMAIL}")
            # Update admin role just in case
            admin.role = ROLE_ADMIN
            admin.password = generate_password_hash(ADMIN_PASSWORD)
            db.session.commit()
            print("Admin credentials updated.")
        else:
            # Create new admin account
            new_admin = User(
                email=ADMIN_EMAIL,
                password=generate_password_hash(ADMIN_PASSWORD),
                name=ADMIN_NAME,
                company=ADMIN_COMPANY,
                role=ROLE_ADMIN
            )
            
            db.session.add(new_admin)
            db.session.commit()
            print(f"Admin account created: {ADMIN_EMAIL}")
        
        print("Admin initialization complete.")
        print(f"Admin email: {ADMIN_EMAIL}")
        print(f"Admin password: {ADMIN_PASSWORD}")

if __name__ == "__main__":
    init_admin()
