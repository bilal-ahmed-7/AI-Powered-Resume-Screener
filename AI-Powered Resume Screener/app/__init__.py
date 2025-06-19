from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.resume_controller import resume_bp
    from app.controllers.job_controller import job_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.admin_controller import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
