from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with Flask application"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here to ensure they are registered with SQLAlchemy
    from app.models import User, Registration
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

def get_db():
    """Helper function to get database instance"""
    return db

def close_db(e=None):
    """Helper function to close database connection"""
    db.session.remove()