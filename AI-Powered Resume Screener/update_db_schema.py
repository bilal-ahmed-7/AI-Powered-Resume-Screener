"""
Database schema update script to add role field to User model and set admin users
"""
import sys
from app import create_app, db
from app.models.user import User, ROLE_CLIENT, ROLE_ADMIN

def update_schema(admin_email=None):
    """
    Update the database schema to include the role field for users
    
    Args:
        admin_email (str, optional): Email of the user to set as admin. If None,
                                    the first user will be set as admin.
    """
    app = create_app()
    
    with app.app_context():
        # Check if we need to add the role column
        try:
            # Try to access the role attribute of the first user
            first_user = User.query.first()
            if first_user:
                print(f"Testing role attribute: {first_user.role}")
                print("Role column already exists.")
                
                # If admin_email is provided, set that user as admin
                if admin_email:
                    user = User.query.filter_by(email=admin_email).first()
                    if user:
                        user.role = ROLE_ADMIN
                        db.session.commit()
                        print(f"User {user.email} has been set as admin.")
                    else:
                        print(f"No user found with email {admin_email}")
                
                return
        except Exception as e:
            # If we get an error, the column doesn't exist
            print(f"Role column doesn't exist: {str(e)}")
            print("Adding role column to users table...")
            
            # Add the role column
            db.engine.execute('ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT "client"')
            print("Role column added successfully.")
            
            # Update existing users
            if admin_email:
                # Set the specified user as admin
                db.engine.execute(f'UPDATE users SET role = "{ROLE_ADMIN}" WHERE email = "{admin_email}"')
                user = User.query.filter_by(email=admin_email).first()
                if user:
                    print(f"User {user.email} has been set as admin.")
                else:
                    print(f"No user found with email {admin_email}")
                    # Make the first user an admin if there are users
                    first_user = User.query.first()
                    if first_user:
                        db.engine.execute(f'UPDATE users SET role = "{ROLE_ADMIN}" WHERE id = {first_user.id}')
                        print(f"User {first_user.email} has been set as admin instead.")
            else:
                # Make the first user an admin if there are users
                first_user = User.query.first()
                if first_user:
                    db.engine.execute(f'UPDATE users SET role = "{ROLE_ADMIN}" WHERE id = {first_user.id}')
                    print(f"User {first_user.email} has been set as admin.")
            
            # Set all other users as clients
            if admin_email:
                db.engine.execute(f'UPDATE users SET role = "{ROLE_CLIENT}" WHERE email != "{admin_email}"')
            else:
                first_user = User.query.first()
                if first_user:
                    db.engine.execute(f'UPDATE users SET role = "{ROLE_CLIENT}" WHERE id != {first_user.id}')
            print("All other users set as clients.")
            
            print("Database schema updated successfully.")

if __name__ == "__main__":
    # Check if an email was provided as a command-line argument
    admin_email = None
    if len(sys.argv) > 1:
        admin_email = sys.argv[1]
        print(f"Setting user with email {admin_email} as admin")
    
    update_schema(admin_email)
