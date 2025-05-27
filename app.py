import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure PostgreSQL connection
# Option 1: For local development (replace with your actual local PostgreSQL credentials)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_pg_user:your_pg_password@localhost/myflaskdb_pg'

# Option 2: For Render deployment (Render will provide DATABASE_URL environment variable for its managed DB)
# The 'postgresql://' scheme is automatically understood by SQLAlchemy.
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith("postgres://"): # Heroku/Render sometimes use "postgres://"
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# Fallback for local development if DATABASE_URL is not set by Render
if not DATABASE_URL:
    print("WARNING: DATABASE_URL not set, using default local PostgreSQL DB.")
    # Replace with your actual local PostgreSQL credentials and database name
    DATABASE_URL = 'postgresql://your_local_pg_user:your_local_pg_password@localhost:5432/myflaskdb_pg'
    # Ensure you have a PostgreSQL server running locally and a database named 'myflaskdb_pg'
    # with user 'your_local_pg_user' and password 'your_local_pg_password'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppresses a warning

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your models (same as before, SQLAlchemy handles the SQL dialect)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Your routes
@app.route('/')
def index():
    return "Hello, World! Connected to PostgreSQL."

@app.route('/add_user/<username>/<email>')
def add_user_route(username, email): # Renamed to avoid conflict with any 'add_user' utility function
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return f"User {username} already exists!"

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return f"Email {email} already exists!"

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return f"User {username} added to PostgreSQL!"
    except Exception as e:
        db.session.rollback()
        return f"Error adding user: {str(e)}"

@app.route('/users')
def get_users():
    try:
        users = User.query.all()
        user_list = "Users in PostgreSQL:<br>"
        for user in users:
            user_list += f"ID: {user.id}, Username: {user.username}, Email: {user.email}<br>"
        return user_list if users else "No users found in PostgreSQL."
    except Exception as e:
        return f"Error fetching users: {str(e)}"

if __name__ == '__main__':
    # Create database tables if they don't exist
    # In a production Render setup, you'd typically use Flask-Migrate and run migrations
    # as part of your deploy process or as a one-off job.
    with app.app_context():
        db.create_all()
    # Render sets the PORT environment variable. Default to 5000 for local dev.
    # Host '0.0.0.0' makes it accessible on your network, which Render requires.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) # Keep debug=True for local, Render might override
