from typing import Dict, Any, List
from app.models.resume import Resume
from app.models.job import Job
from app.models.offer_letter import OfferLetter
from datetime import datetime

class AIProcessor:
    """
    Processes resume and job data to extract features for matching.
    """
    
    def __init__(self):
        """Initialize the AI processor."""
        # You could add more sophisticated NLP models here in the future
        pass
    
    def process_resume(self, resume: Resume) -> Dict[str, Any]:
        """
        Process a resume to extract features for matching.
        
        Args:
            resume: A Resume object
            
        Returns:
            Dictionary containing processed resume features
        """
        # Extract skills as a list
        skills = resume.skills.split(',') if resume.skills else []
        
        # Create a feature dictionary
        features = {
            'skills': skills,
            'experience': resume.experience,
            'education': resume.education,
            'candidate_name': resume.candidate_name,
            'resume_id': resume.id
        }
        
        return features
    
    def process_job(self, job: Job) -> Dict[str, Any]:
        """
        Process a job to extract features for matching.
        
        Args:
            job: A Job object
            
        Returns:
            Dictionary containing processed job features
        """
        # Extract required skills as a list
        required_skills = job.required_skills.split(',') if job.required_skills else []
        
        # Create a feature dictionary
        features = {
            'title': job.title,
            'description': job.description,
            'required_skills': required_skills,
            'required_experience': job.required_experience,
            'required_education': job.required_education,
            'job_id': job.id
        }
        
        return features
        
    def generate_offer_letter(self, resume: Resume, job: Job, admin_id: int) -> Dict[str, Any]:
        """
        Generate an AI-based offer letter for a candidate based on their resume and the job.
        
        Args:
            resume: A Resume object
            job: A Job object
            admin_id: ID of the admin generating the offer
            
        Returns:
            Dictionary containing the offer letter content and metadata
        """
        # Extract candidate name and job title
        candidate_name = resume.candidate_name
        job_title = job.title
        company_name = job.company_name if hasattr(job, 'company_name') and job.company_name else "Our Company"
        
        # Generate current date in a formal format
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Generate a personalized offer letter
        letter_content = f"""
{current_date}

Dear {candidate_name},

We are pleased to offer you the position of {job_title} at {company_name}. After careful review of your qualifications and experience, we believe you would be an excellent addition to our team.

Based on your impressive background in {resume.experience if resume.experience else 'your field'} and your skills in {resume.skills if resume.skills else 'relevant areas'}, we are confident that you will contribute significantly to our organization.

This offer includes:
- Position: {job_title}
- Start Date: To be determined upon acceptance
- Compensation: Competitive salary based on your experience and qualifications
- Benefits: Health insurance, retirement plan, and paid time off

Please review the attached detailed offer package and let us know your decision within the next 7 days.

We look forward to welcoming you to our team!

Sincerely,
The {company_name} Team
        """
        
        # Create an offer letter object
        offer_letter = {
            'resume_id': resume.id,
            'job_id': job.id,
            'admin_id': admin_id,
            'content': letter_content,
            'created_date': datetime.now()
        }
        
        return offer_letter
