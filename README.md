# Clipper Affiliate Platform

A responsive web platform for managing short-form content creators in the DACH region.

## Features

- **Responsive Design**: Mobile-first approach with full device support
- **User Roles**: Admin, Manager, and Clipper roles with appropriate permissions
- **Project Management**: Create and manage campaigns with different payment models
- **Submission Tracking**: Track video submissions and payouts
- **Telegram Integration**: WebApp SDK support for Telegram Mini App functionality

## Tech Stack

- **Backend**: Flask 3.0.2 with SQLAlchemy
- **Frontend**: Bootstrap 5.3.3 with custom responsive CSS
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Flask-Login with bcrypt password hashing
- **Deployment**: Gunicorn WSGI server

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   - `SECRET_KEY`: Your Flask secret key
   - `DATABASE_URL`: PostgreSQL connection string
   - `ADMIN_EMAILS`: Comma-separated admin email list
4. Initialize database: The app will auto-create tables on first run
5. Run locally: `python run.py`

## Deployment

The app is configured for deployment on platforms like Heroku, Render, or any PaaS supporting Python web applications.

### Environment Variables Required

- `SECRET_KEY`: Flask application secret
- `DATABASE_URL`: PostgreSQL connection URL
- `ADMIN_EMAILS`: Admin user email addresses

## Default Admin

After deployment, an admin user will be created automatically:
- Email: `admin@clipper.io`
- Password: `admin123`

**Important**: Change the default admin password after first login.

## Mobile Responsiveness

The platform is fully responsive with:
- Mobile navigation with hamburger menu
- Touch-friendly interface elements
- Optimized layouts for all screen sizes
- Proper viewport configuration

## Telegram Mini App

The platform includes Telegram WebApp SDK integration for Mini App functionality.
