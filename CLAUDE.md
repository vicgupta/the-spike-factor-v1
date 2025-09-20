# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
- `python3 -m venv venv` - Create virtual environment
- `source venv/bin/activate` - Activate virtual environment
- `pip install -r requirements.txt` - Install dependencies

### Database Management
- `flask db init` - Initialize database migrations (already done)
- `flask db migrate -m "message"` - Create new migration
- `flask db upgrade` - Apply migrations
- `flask db downgrade` - Rollback migrations

### Running the Application

#### Development
- `python app.py` - Start development server on http://127.0.0.1:5000
- `flask run` - Alternative way to start the server

#### Production
- `gunicorn wsgi:app` - Start production server with Gunicorn
- `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app` - Start with 4 workers on port 8000
- `gunicorn --bind 127.0.0.1:5000 --workers 3 wsgi:app` - Local production setup

### Testing
- `pytest` - Run all tests (when test files are created)
- `pytest tests/` - Run specific test directory

## Project Architecture

### Core Structure
This is a Flask web application implementing "The Spike Factor" personality assessment platform with the following architecture:

**Application Factory Pattern**: Uses `create_app()` function in `app/__init__.py` to configure the Flask application with blueprints and extensions.

**Blueprint Organization**:
- `auth` - Authentication (login, register, logout)
- `dashboard` - User dashboard and overview
- `assessment` - Assessment taking and management
- `reports` - Report viewing and management

**Database Models** (SQLAlchemy ORM):
- `User` - User accounts with email/password authentication
- `Assessment` - Assessment instances linked to users
- `Response` - Individual question responses within assessments
- `Report` - Generated reports based on completed assessments

### Key Components

**Authentication System**: Flask-Login provides session management with login/logout functionality and login_required decorators for protected routes.

**Assessment Flow**:
1. User starts assessment (`/assessment/simple`)
2. Questions presented one-by-one with progress tracking
3. Responses stored in database
4. Report automatically generated on completion using scoring algorithm

**Scoring Algorithm** (`app/assessment/scoring.py`):
- Converts Likert scale responses to numerical scores
- Calculates overall "spike factor" percentage
- Generates personality insights with strengths, growth areas, and recommendations

**Frontend**: Bootstrap 5 with custom CSS for responsive design and modern UI components.

### Configuration
- Environment variables stored in `.env` file
- Flask config in `config.py` with settings for database, email, and security
- SQLite database for development (configurable via DATABASE_URL)

### Template Structure
- `templates/base.html` - Common layout with navigation and Bootstrap styling
- Blueprint-specific template directories mirror the application structure
- Responsive design with mobile-first approach

### Security Features
- CSRF protection via Flask-WTF
- Password hashing with Werkzeug
- Email validation on registration
- Session-based authentication

## Development Notes

- The application uses SQLite by default but can be configured for other databases via DATABASE_URL
- Email functionality is configured but requires valid SMTP settings in .env
- Assessment questions are currently hardcoded in `assessment/routes.py` but can be moved to database
- Report generation is immediate and stored in database for future viewing
- All routes require authentication except landing page and auth routes