from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import db
from app.models.user import User, ROLE_ADMIN, ROLE_CLIENT
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Custom decorators for role-based access control
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and is an admin
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check if admin PIN has been verified
        if not session.get('admin_pin_verified'):
            flash('Please enter the admin PIN to access this page.', 'warning')
            return redirect(url_for('auth.admin_pin'))
            
        return f(*args, **kwargs)
    return decorated_function

def client_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_client():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('resume.dashboard'))
    
    # Only allow client registration through the normal registration process
    # Admin account is created automatically by the system
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        company = request.form.get('company')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new client user
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            company=company,
            role=ROLE_CLIENT  # Always create clients through registration
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login', role='client'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('resume.dashboard'))
    
    # Get role from query parameter
    requested_role = request.args.get('role', 'client')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Hardcoded admin credentials check
        if email == 'admin@gmail.com' and password == 'admin123':
            # Check if this admin exists in the database
            admin_user = User.query.filter_by(email=email).first()
            
            # If admin doesn't exist in the database, create it
            if not admin_user:
                admin_user = User(
                    email=email,
                    password=generate_password_hash(password),
                    name='Admin',
                    company='System',
                    role=ROLE_ADMIN
                )
                db.session.add(admin_user)
                db.session.commit()
            # If admin exists but password doesn't match the hardcoded one, use it anyway
            login_user(admin_user, remember=remember)
            admin_user.last_login = datetime.now()
            db.session.commit()
            # Redirect to PIN verification page instead of dashboard
            return redirect(url_for('auth.admin_pin'))
        
        # Regular user authentication
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login', role=requested_role))
        
        # Only check if a non-admin is trying to access the admin login
        if requested_role == ROLE_ADMIN and not user.is_admin():
            flash('You do not have admin privileges.', 'danger')
            return redirect(url_for('auth.login', role=requested_role))
        
        login_user(user, remember=remember)
        user.last_login = datetime.now()
        db.session.commit()
        
        next_page = request.args.get('next')
        
        # Redirect based on role
        if user.is_admin():
            # Redirect admin users to PIN verification page
            return redirect(next_page or url_for('auth.admin_pin'))
        else:
            return redirect(next_page or url_for('resume.dashboard'))
    
    # Display appropriate login template based on role
    if requested_role == ROLE_ADMIN:
        return render_template('auth/admin_login.html')
    else:
        return render_template('auth/login.html', requested_role=requested_role)

@auth_bp.route('/admin/pin', methods=['GET', 'POST'])
@login_required
def admin_pin():
    # Only allow admin users to access this page
    if not current_user.is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    # If PIN is already verified, redirect to admin dashboard
    if session.get('admin_pin_verified'):
        return redirect(url_for('admin.dashboard'))
    
    # Handle POST request (PIN verification)
    if request.method == 'POST':
        pin = request.form.get('pin')
        
        # Verify the PIN (hardcoded as '1234')
        if pin == '1234':
            # Set session variable to indicate PIN has been verified
            session['admin_pin_verified'] = True
            flash('PIN verified successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid PIN. Please try again.', 'danger')
            return redirect(url_for('auth.admin_pin'))
    
    # Handle GET request (show PIN form)
    return render_template('auth/admin_pin.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Clear admin PIN verification status
    session.pop('admin_pin_verified', None)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        
        current_user.name = name
        current_user.company = company
        
        # Only allow admins to change roles, and only for themselves
        if current_user.is_admin() and request.form.get('role'):
            current_user.role = request.form.get('role')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    return render_template('auth/profile.html')


@auth_bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_admin():
    """Only admins can create other admin accounts"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        company = request.form.get('company')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.create_admin'))
        
        # Create new admin user
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            company=company,
            role=ROLE_ADMIN
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('auth/create_admin.html')
