from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models.job import Job
from app.models.resume import Resume
from app.controllers.auth_controller import admin_required

job_bp = Blueprint('job', __name__, url_prefix='/job')

@job_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_job():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        company = request.form.get('company')
        description = request.form.get('description')
        required_skills = request.form.get('required_skills')
        required_experience = request.form.get('required_experience')
        required_education = request.form.get('required_education')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        salary_range = request.form.get('salary_range')
        
        # Create new job
        new_job = Job(
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            required_experience=required_experience,
            required_education=required_education,
            location=location,
            job_type=job_type,
            salary_range=salary_range,
            user_id=current_user.id,
            created_date=datetime.now()
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job created successfully!', 'success')
        return redirect(url_for('resume.dashboard'))
    
    return render_template('job/create.html')

@job_bp.route('/<int:job_id>')
@login_required
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Different behavior based on user role
    if current_user.is_admin():
        # Admins can view any job and see all resumes for matching
        resumes = Resume.query.all()
    else:
        # Clients can view any job but only see their own resumes for matching
        resumes = Resume.query.filter_by(user_id=current_user.id).all()
    
    # Placeholder for statistics (in a real app, these would be calculated from actual data)
    matches = 0
    high_matches = 0
    avg_score = 0
    
    return render_template('job/view.html', 
                           job=job, 
                           resumes=resumes,
                           matches=matches,
                           high_matches=high_matches,
                           avg_score=avg_score)

@job_bp.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if request.method == 'POST':
        # Update job with form data
        job.title = request.form.get('title')
        job.company = request.form.get('company')
        job.description = request.form.get('description')
        job.required_skills = request.form.get('required_skills')
        job.required_experience = request.form.get('required_experience')
        job.required_education = request.form.get('required_education')
        job.location = request.form.get('location')
        job.job_type = request.form.get('job_type')
        job.salary_range = request.form.get('salary_range')
        job.last_updated = datetime.now()
        
        db.session.commit()
        
        flash('Job updated successfully!', 'success')
        return redirect(url_for('job.view_job', job_id=job.id))
    
    return render_template('job/edit.html', job=job)

@job_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    # Check if user is admin before allowing deletion
    if not current_user.is_admin():
        flash('You do not have permission to delete jobs', 'danger')
        return redirect(url_for('job.view_job', job_id=job_id))
    
    job = Job.query.get_or_404(job_id)
    
    try:
        db.session.delete(job)
        db.session.commit()
        flash('Job deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting job: {str(e)}', 'danger')
    
    return redirect(url_for('resume.dashboard'))

@job_bp.route('/list')
@login_required
def list_jobs():
    # Show all jobs regardless of user role
    jobs = Job.query.all()
    return render_template('job/list.html', jobs=jobs, is_admin=current_user.is_admin())
