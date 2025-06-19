from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from app import db
from app.models.resume import Resume
from app.models.job import Job
from app.models.feedback import Feedback
from app.models.offer_letter import OfferLetter
from app.services.resume_parser import ResumeParser
from app.services.ai_processor import AIProcessor
from app.services.scoring_service import ScoringService
from app.utils.file_utils import allowed_file
from app.controllers.auth_controller import client_required

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

@resume_bp.route('/dashboard')
@login_required
@client_required
def dashboard():
    from datetime import datetime
    
    # For clients, show their resumes and all available jobs
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    jobs = Job.query.all()  # Show all jobs, not just their own
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Get resume IDs for this user
    resume_ids = [resume.id for resume in resumes]
    
    # Count matches (placeholder - you might need to implement this properly)
    matches = 0
    
    return render_template('resume/dashboard.html', 
                           resumes=resumes, 
                           jobs=jobs, 
                           current_date=current_date,
                           matches=matches)

@resume_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@client_required
def upload_resume():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['resume']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Generate a unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save the file
            file.save(file_path)
            
            # Parse the resume
            parser = ResumeParser()
            resume_data = parser.parse(file_path)
            
            # Create a new resume record
            new_resume = Resume(
                filename=filename,
                file_path=unique_filename,
                user_id=current_user.id,
                candidate_name=resume_data.get('name', ''),
                email=resume_data.get('email', ''),
                phone=resume_data.get('phone', ''),
                skills=','.join(resume_data.get('skills', [])),
                experience=resume_data.get('experience', ''),
                education=resume_data.get('education', ''),
                upload_date=datetime.now()
            )
            
            db.session.add(new_resume)
            db.session.commit()
            
            flash('Resume uploaded successfully!', 'success')
            return redirect(url_for('resume.view_resume', resume_id=new_resume.id))
        else:
            flash('File type not allowed', 'danger')
            return redirect(request.url)
    
    return render_template('resume/upload.html')

@resume_bp.route('/<int:resume_id>')
@login_required
@client_required
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if the resume belongs to the current user
    if resume.user_id != current_user.id:
        flash('You do not have permission to view this resume', 'danger')
        return redirect(url_for('resume.dashboard'))
    
    # Get all jobs for matching section (clients can see all jobs)
    jobs = Job.query.all()
    
    # Get feedback for this resume
    feedback_messages = Feedback.query.filter_by(resume_id=resume_id).order_by(Feedback.created_date.desc()).all()
    
    # Mark unread feedback as read
    unread_feedback = Feedback.query.filter_by(resume_id=resume_id, read=False).all()
    for feedback in unread_feedback:
        feedback.read = True
    
    if unread_feedback:
        db.session.commit()
    
    return render_template('resume/view.html', resume=resume, jobs=jobs, feedback_messages=feedback_messages)

# Matching functionality moved to admin controller

@resume_bp.route('/<int:resume_id>/delete', methods=['POST'])
@login_required
@client_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if the resume belongs to the current user
    if resume.user_id != current_user.id:
        flash('You do not have permission to delete this resume', 'danger')
        return redirect(url_for('resume.dashboard'))
    
    # Delete the file
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], resume.file_path))
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'warning')
    
    # Delete the database record
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully', 'success')
    return redirect(url_for('resume.dashboard'))

@resume_bp.route('/list')
@login_required
@client_required
def list_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('resume/list.html', resumes=resumes)

@resume_bp.route('/offer-letters')
@login_required
@client_required
def list_offer_letters():
    # Get all resumes for the current user
    user_resumes = Resume.query.filter_by(user_id=current_user.id).all()
    
    # Get all resume IDs
    resume_ids = [resume.id for resume in user_resumes]
    
    # Get all offer letters for these resumes
    offer_letters = OfferLetter.query.filter(OfferLetter.resume_id.in_(resume_ids)).order_by(OfferLetter.created_date.desc()).all()
    
    return render_template('resume/offer_letters.html', offer_letters=offer_letters)

@resume_bp.route('/offer-letter/<int:letter_id>')
@login_required
@client_required
def view_offer_letter(letter_id):
    # Get the offer letter
    offer_letter = OfferLetter.query.get_or_404(letter_id)
    
    # Check if the offer letter is for one of the user's resumes
    resume = Resume.query.get_or_404(offer_letter.resume_id)
    if resume.user_id != current_user.id:
        flash('You do not have permission to view this offer letter', 'danger')
        return redirect(url_for('resume.list_offer_letters'))
    
    return render_template('resume/view_offer_letter.html', offer_letter=offer_letter)

@resume_bp.route('/offer-letter/<int:letter_id>/respond', methods=['POST'])
@login_required
@client_required
def respond_to_offer_letter(letter_id):
    # Get the offer letter
    offer_letter = OfferLetter.query.get_or_404(letter_id)
    
    # Check if the offer letter is for one of the user's resumes
    resume = Resume.query.get_or_404(offer_letter.resume_id)
    if resume.user_id != current_user.id:
        flash('You do not have permission to respond to this offer letter', 'danger')
        return redirect(url_for('resume.list_offer_letters'))
    
    # Update the status based on the response
    response = request.form.get('response')
    if response in ['accepted', 'rejected']:
        offer_letter.status = response
        offer_letter.response_date = datetime.now()
        db.session.commit()
        
        flash(f'You have {response} the offer letter', 'success')
    else:
        flash('Invalid response', 'danger')
    
    return redirect(url_for('resume.view_offer_letter', letter_id=letter_id))
