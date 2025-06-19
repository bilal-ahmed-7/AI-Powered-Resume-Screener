import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: The name of the file to check
        
    Returns:
        Boolean indicating if the file has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_extension(filename):
    """
    Get the extension of a file.
    
    Args:
        filename: The name of the file
        
    Returns:
        The file extension (without the dot)
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def create_upload_directories():
    """
    Create necessary upload directories if they don't exist.
    """
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
