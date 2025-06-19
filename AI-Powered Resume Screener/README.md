# AI-Powered Resume Screener

## Project Overview

The AI-Powered Resume Screener is a web application that helps recruiters and hiring managers streamline the resume screening process by automatically matching candidate resumes with job requirements. The system uses natural language processing and machine learning techniques to analyze resumes and job descriptions, providing a match score and detailed feedback.

## Features

### Role-Based Authentication System
- **Admin Role**: Full access to manage jobs, view all resumes, and perform matching operations
- **Client Role**: Upload and manage personal resumes, view available jobs
- **Secure Login**: Password hashing and session management for secure authentication

### Resume Management
- Upload resumes in various formats (PDF, DOCX)
- Automatic extraction of key information (skills, experience, education)
- Organize and view uploaded resumes

### Job Management
- Create, edit, and delete job postings (admin only)
- Specify job requirements including skills, experience, and education
- View detailed job information

### AI-Powered Matching
- Match resumes against job requirements
- Generate match scores based on skills, experience, and education alignment
- Provide detailed feedback and improvement suggestions

### AI-Generated Offer Letters
- Admins can approve resumes and generate personalized offer letters
- AI-powered content generation based on candidate qualifications and job details
- Users can view, accept, or reject offer letters from their dashboard
- Print or email functionality for offer letters

### User-Friendly Interface
- Responsive design for desktop and mobile devices
- Intuitive navigation and clear information presentation
- Role-specific dashboards and views

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLAlchemy ORM with SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **AI Components**: Custom NLP services for text processing and matching

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-powered-resume-screener.git
   cd ai-powered-resume-screener
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python update_db_schema.py
   ```

5. Create the admin account:
   ```
   python init_admin.py
   ```

6. Run the application:
   ```
   python main.py
   ```

7. Access the application at `http://127.0.0.1:5000`

## Usage Guide

### Admin Access
- **Login**: Use the credentials created during setup (default: admin123@gmail.com / admin123)
- **Dashboard**: View system statistics and recent activity
- **Job Management**: Create, edit, and delete jobs
- **Resume Management**: View all user resumes and match them with jobs
- **User Management**: View and manage user accounts

### Client Access
- **Registration**: Create a new account as a client
- **Resume Upload**: Upload and manage personal resumes
- **Job Browsing**: View available job postings
- **Profile Management**: Update personal information

## Project Structure

```
ai-powered-resume-screener/
├── app/
│   ├── controllers/       # Route handlers and business logic
│   ├── models/            # Database models
│   ├── services/          # AI and utility services
│   ├── static/            # CSS, JS, and static assets
│   ├── templates/         # HTML templates
│   └── __init__.py        # Application factory
├── migrations/            # Database migrations
├── tests/                 # Test suite
├── init_admin.py          # Admin initialization script
├── main.py                # Application entry point
├── requirements.txt       # Project dependencies
├── truncate_db.py         # Database reset utility
└── update_db_schema.py    # Database schema update utility
```

## Security Considerations

- Passwords are securely hashed before storage
- Role-based access control prevents unauthorized operations
- Input validation and sanitization to prevent injection attacks
- Secure file upload handling to prevent malicious file uploads

## Future Enhancements

### AI and Machine Learning
- Enhanced AI matching algorithms with deep learning models
- Resume parsing improvements using advanced NLP techniques
- Sentiment analysis for candidate communications
- Predictive analytics for candidate success probability
- AI-powered interview question generation based on resume gaps

### Integration and Connectivity
- API integration with job boards and applicant tracking systems
- Calendar integration for scheduling interviews
- Integration with HR management systems
- Social media profile analysis and integration
- Video interview platform integration

### User Experience
- Mobile app development for on-the-go access
- Real-time chat between candidates and recruiters
- Interactive dashboard with data visualization
- Customizable email templates and notification preferences
- Multi-language support for international recruitment

### Advanced Features
- Automated reference checking system
- Candidate onboarding workflow after offer acceptance
- Contract generation and digital signing
- Salary negotiation assistant
- Compliance checking for job descriptions and hiring practices

### Security and Compliance
- GDPR and other regional compliance features
- Enhanced data encryption and privacy controls
- Candidate data retention policies and automation
- Audit trails for all system actions
- Two-factor authentication for enhanced security

## Acknowledgments

- Flask and SQLAlchemy communities for excellent documentation
- Bootstrap team for the responsive UI framework
- Open source NLP libraries that made the AI features possible

