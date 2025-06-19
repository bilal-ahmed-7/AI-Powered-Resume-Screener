from datetime import datetime
from app import db

class Resume(db.Model):
    """Model representing a resume uploaded by a user."""
    
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Parsed resume data
    candidate_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)  # Comma-separated list of skills
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    
    # Metadata
    upload_date = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Resume {self.id}: {self.filename}>"
