from datetime import datetime
from app import db

class Job(db.Model):
    """Model representing a job posting created by a user."""
    
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)  # Comma-separated list of required skills
    required_experience = db.Column(db.String(100))
    required_education = db.Column(db.String(100))
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract, etc.
    salary_range = db.Column(db.String(100))
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Metadata
    created_date = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<Job {self.id}: {self.title} at {self.company}>"
