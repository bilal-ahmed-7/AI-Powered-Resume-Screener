from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User, ROLE_ADMIN, ROLE_CLIENT
from app.models.job import Job
from app.models.resume import Resume
from app.models.feedback import Feedback
from app.models.offer_letter import OfferLetter
from app.controllers.auth_controller import admin_required
from datetime import datetime
from app.services.ai_processor import AIProcessor
from app.services.scoring_service import ScoringService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard showing system overview"""
    # Get counts for dashboard stats
    user_count = User.query.count()
    client_count = User.query.filter_by(role=ROLE_CLIENT).count()
    admin_count = User.query.filter_by(role=ROLE_ADMIN).count()
    job_count = Job.query.count()
    resume_count = Resume.query.count()
    
    # Get recent activity
    recent_jobs = Job.query.order_by(Job.created_date.desc()).limit(5).all()
    recent_resumes = Resume.query.order_by(Resume.upload_date.desc()).limit(5).all()
    # Only show client users, not admins
    recent_users = User.query.filter_by(role=ROLE_CLIENT).order_by(User.created_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                          user_count=user_count,
                          client_count=client_count,
                          admin_count=admin_count,
                          job_count=job_count,
                          resume_count=resume_count,
                          recent_jobs=recent_jobs,
                          recent_resumes=recent_resumes,
                          recent_users=recent_users,
                          current_date=datetime.now().strftime('%B %d, %Y'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Admin view of all users"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle_role', methods=['POST'])
@login_required
@admin_required
def toggle_user_role(user_id):
    """Toggle a user between client and admin roles"""
    user = User.query.get_or_404(user_id)
    
    # Don't allow changing your own role
    if user.id == current_user.id:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('admin.users'))
    
    # Toggle the role
    if user.role == ROLE_ADMIN:
        user.role = ROLE_CLIENT
        flash(f'User {user.email} is now a client.', 'success')
    else:
        user.role = ROLE_ADMIN
        flash(f'User {user.email} is now an admin.', 'success')
    
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle_active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    """Toggle a user's active status"""
    user = User.query.get_or_404(user_id)
    
    # Don't allow deactivating yourself
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    status = 'activated' if user.is_active else 'deactivated'
    
    db.session.commit()
    flash(f'User {user.email} has been {status}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/resumes')
@login_required
@admin_required
def all_resumes():
    """Admin view of all resumes in the system"""
    resumes = Resume.query.all()
    return render_template('admin/resumes.html', resumes=resumes)

@admin_bp.route('/jobs')
@login_required
@admin_required
def all_jobs():
    """Admin view of all jobs in the system"""
    jobs = Job.query.all()
    return render_template('admin/jobs.html', jobs=jobs)

@admin_bp.route('/resume/<int:resume_id>')
@login_required
@admin_required
def view_resume(resume_id):
    """Admin view of a specific resume"""
    resume = Resume.query.get_or_404(resume_id)
    jobs = Job.query.all()  # Admin can match with any job
    
    # Get previous feedback for this resume
    previous_feedback = Feedback.query.filter_by(resume_id=resume_id).order_by(Feedback.created_date.desc()).all()
    
    return render_template('admin/view_resume.html', resume=resume, jobs=jobs, previous_feedback=previous_feedback)

@admin_bp.route('/job/<int:job_id>')
@login_required
@admin_required
def view_job(job_id):
    """Admin view of a specific job"""
    job = Job.query.get_or_404(job_id)
    resumes = Resume.query.all()  # Admin can match with any resume
    
    return render_template('admin/view_job.html', job=job, resumes=resumes)

@admin_bp.route('/resume/<int:resume_id>/send_feedback', methods=['POST'])
@login_required
@admin_required
def send_feedback(resume_id):
    """Admin function to send feedback to a user about their resume"""
    resume = Resume.query.get_or_404(resume_id)
    message = request.form.get('message', '').strip()
    
    if not message:
        flash('Feedback message cannot be empty', 'danger')
        return redirect(url_for('admin.view_resume', resume_id=resume_id))
    
    # Create new feedback
    feedback = Feedback(
        resume_id=resume_id,
        admin_id=current_user.id,
        message=message,
        created_date=datetime.now()
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    flash('Feedback sent successfully', 'success')
    return redirect(url_for('admin.view_resume', resume_id=resume_id))

@admin_bp.route('/resume/<int:resume_id>/match/<int:job_id>')
@login_required
@admin_required
def match_resume_to_job(resume_id, job_id):
    """Admin function to match a resume to a job"""
    resume = Resume.query.get_or_404(resume_id)
    job = Job.query.get_or_404(job_id)
    
    # Get AI processor and scoring service
    ai_processor = AIProcessor()
    scoring_service = ScoringService()
    
    # Process resume and job description
    resume_features = ai_processor.process_resume(resume)
    job_features = ai_processor.process_job(job)
    
    # Calculate match score
    match_score, match_details = scoring_service.calculate_match_score(resume_features, job_features)
    
    # Format match details for the template
    formatted_match_details = {
        'skills': {
            'score': match_details.get('skill_score', 0),
            'explanation': f"Matched {len(match_details.get('matching_skills', []))} out of {len(job_features.get('required_skills', []))} required skills.",
            'improvement_suggestion': f"Consider acquiring skills in: {', '.join(match_details.get('missing_skills', []))}" if match_details.get('missing_skills') else "No specific skill improvements needed."
        },
        'experience': {
            'score': match_details.get('experience_score', 0),
            'explanation': f"Experience level is {match_details.get('experience_score', 0)}% aligned with job requirements.",
            'improvement_suggestion': "Consider gaining more experience in this field." if match_details.get('experience_score', 0) < 70 else "Experience level is sufficient."
        },
        'education': {
            'score': match_details.get('education_score', 0),
            'explanation': f"Education level is {match_details.get('education_score', 0)}% aligned with job requirements.",
            'improvement_suggestion': "Consider pursuing higher education in this field." if match_details.get('education_score', 0) < 70 else "Education level is sufficient."
        }
    }
    
    return render_template('admin/match_result.html', 
                          resume=resume, 
                          job=job, 
                          match_score=match_score, 
                          match_details=formatted_match_details)

@admin_bp.route('/resume/<int:resume_id>/approve/<int:job_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def approve_resume(resume_id, job_id):
    """Admin function to approve a resume and generate an offer letter"""
    resume = Resume.query.get_or_404(resume_id)
    job = Job.query.get_or_404(job_id)
    
    if request.method == 'POST':
        # Generate an offer letter
        ai_processor = AIProcessor()
        offer_letter_data = ai_processor.generate_offer_letter(resume, job, current_user.id)
        
        # Create a new offer letter record
        new_offer = OfferLetter(
            resume_id=offer_letter_data['resume_id'],
            job_id=offer_letter_data['job_id'],
            admin_id=offer_letter_data['admin_id'],
            content=offer_letter_data['content'],
            created_date=offer_letter_data['created_date']
        )
        
        db.session.add(new_offer)
        db.session.commit()
        
        flash('Resume approved and offer letter sent successfully!', 'success')
        return redirect(url_for('admin.view_offer_letter', offer_id=new_offer.id))
    
    return render_template('admin/approve_resume.html', resume=resume, job=job)

@admin_bp.route('/offer_letters')
@login_required
@admin_required
def all_offer_letters():
    """Admin view of all offer letters in the system"""
    offer_letters = OfferLetter.query.all()
    return render_template('admin/offer_letters.html', offer_letters=offer_letters)

@admin_bp.route('/offer_letter/<int:offer_id>')
@login_required
@admin_required
def view_offer_letter(offer_id):
    """Admin view of a specific offer letter"""
    offer_letter = OfferLetter.query.get_or_404(offer_id)
    return render_template('admin/view_offer_letter.html', offer_letter=offer_letter)
