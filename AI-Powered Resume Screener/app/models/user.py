from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# Define user roles
ROLE_CLIENT = 'client'
ROLE_ADMIN = 'admin'

class User(UserMixin, db.Model):
    """Model representing a user of the application."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    role = db.Column(db.String(20), default=ROLE_CLIENT)  # Default role is client
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy='dynamic')
    jobs = db.relationship('Job', backref='user', lazy='dynamic')
    
    # Metadata
    created_date = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Role-based methods
    def is_admin(self):
        return self.role == ROLE_ADMIN
        
    def is_client(self):
        return self.role == ROLE_CLIENT
    
    def __repr__(self):
        return f"<User {self.email}>"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
