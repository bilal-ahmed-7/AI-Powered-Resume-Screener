import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.feedback import Feedback
from app.models.offer_letter import OfferLetter

# Create app context
app = create_app()

# Create database tables
with app.app_context():
    # Import all models here to ensure they're registered with SQLAlchemy
    print("Updating database schema...")
    db.create_all()
    print("Database schema updated successfully!")
    
    # Check if the feedback table was created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    if 'feedback' in tables:
        print("Feedback table created successfully.")
    else:
        print("Warning: Feedback table was not created.")
    
    if 'offer_letters' in tables:
        print("Offer Letters table created successfully.")
    else:
        print("Warning: Offer Letters table was not created.")
        
    print(f"Available tables: {', '.join(tables)}")
