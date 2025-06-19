import os
import sqlite3
from app import create_app, db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.feedback import Feedback
from app.models.offer_letter import OfferLetter

app = create_app()

# Get the database path from the app config
with app.app_context():
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    # If it's a relative path, make it absolute
    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', db_path)
    
    print(f"Database path: {db_path}")
    
    # Check if the database exists
    db_exists = os.path.exists(db_path)
    
    if db_exists:
        print(f"Found existing database at {db_path}")
        
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Drop all tables
            for table in tables:
                if table[0] != 'sqlite_sequence':
                    print(f"Dropping table: {table[0]}")
                    cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
            
            conn.commit()
            conn.close()
            print("All tables dropped successfully")
        except Exception as e:
            print(f"Error dropping tables: {e}")
    
    # Create all tables based on the current models
    try:
        db.create_all()
        print("All tables created successfully with the current models")
    except Exception as e:
        print(f"Error creating tables: {e}")

