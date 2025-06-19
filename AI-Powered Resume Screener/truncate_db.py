"""
Script to truncate all tables in the database without removing any code
"""
from app import create_app, db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.offer_letter import OfferLetter

def truncate_database():
    """Truncate all tables in the database"""
    app = create_app()
    
    with app.app_context():
        # Delete all records from all tables
        print("Truncating database tables...")
        
        # Delete in order to respect foreign key constraints
        print("Deleting offer letters...")
        OfferLetter.query.delete()
        
        print("Deleting resumes...")
        Resume.query.delete()
        
        print("Deleting jobs...")
        Job.query.delete()
        
        print("Deleting users...")
        User.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        print("All tables have been truncated successfully.")
        print("You can now run init_admin.py to create the admin account again.")

if __name__ == "__main__":
    truncate_database()
