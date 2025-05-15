from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Create tables within app context
    with app.app_context():
        # Import all models here
        from .user import User
        from .models import Registration, Document
        
        # Create all tables
        db.create_all()
        return db