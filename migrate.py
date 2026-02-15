"""Database migration script for Render deployment"""

import os
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
