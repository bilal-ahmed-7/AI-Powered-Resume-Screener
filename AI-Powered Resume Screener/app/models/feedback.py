from datetime import datetime
from app import db

class Feedback(db.Model):
    """Model representing feedback/messages from admin to users about their resumes."""
    
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    resume = db.relationship('Resume', backref=db.backref('feedback', lazy='dynamic'))
    admin = db.relationship('User', backref=db.backref('sent_feedback', lazy='dynamic'))
    
    def __repr__(self):
        return f"<Feedback {self.id} for Resume {self.resume_id}>"
