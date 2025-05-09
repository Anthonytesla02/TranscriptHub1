import os
import sys
import sqlite3
from main import app, db
from models import User
from werkzeug.security import generate_password_hash
from config import IS_VERCEL, DATABASE_TYPE

# Initialize SQLite database file for Vercel deployment
if IS_VERCEL and DATABASE_TYPE == 'sqlite':
    try:
        print("Setting up SQLite database for Vercel...")
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname('transcripthub.db')
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        # Create tables if they don't exist
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            
            # Check if test user exists, if not create one
            if not User.query.filter_by(username='testuser').first():
                print("Creating test user...")
                test_user = User(username='testuser', password=generate_password_hash('password123'))
                db.session.add(test_user)
                db.session.commit()
                print("Test user created successfully.")
                
        print("SQLite database setup completed")
    except Exception as e:
        print(f"Error setting up SQLite database: {str(e)}")
        # Don't crash the app if database setup fails
        print("Continuing with app startup despite database setup error")

# This is for both local and Vercel deployment
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))