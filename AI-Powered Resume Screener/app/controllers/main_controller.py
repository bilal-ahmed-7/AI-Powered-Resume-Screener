from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirect to client login page
    return redirect(url_for('auth.login', role='client'))

@main_bp.route('/admin')
def admin_login():
    # Redirect to admin login page
    return redirect(url_for('auth.login', role='admin'))
