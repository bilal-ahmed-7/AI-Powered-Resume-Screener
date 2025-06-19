import sys
import os

# Add the parent directory to the path so we can import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from app import create_app, db
from app.models.feedback import Feedback

# Create app context
app = create_app()

# Create database tables
with app.app_context():
    # Create the feedback table
    db.create_all()
    print("Database schema updated with feedback table.")
