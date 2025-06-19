from datetime import datetime
from app import db

class OfferLetter(db.Model):
    """Model representing an offer letter sent to a candidate."""
    
    __tablename__ = 'offer_letters'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='sent')  # sent, accepted, rejected
    created_date = db.Column(db.DateTime, default=datetime.now)
    response_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    resume = db.relationship('Resume', backref=db.backref('offer_letters', lazy='dynamic'))
    job = db.relationship('Job', backref=db.backref('offer_letters', lazy='dynamic'))
    admin = db.relationship('User', backref=db.backref('sent_offers', lazy='dynamic'))
    
    def __repr__(self):
        return f"<OfferLetter {self.id} for Resume {self.resume_id}, Job {self.job_id}>"
