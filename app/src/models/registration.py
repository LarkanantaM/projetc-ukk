from datetime import datetime
from app.src.database import db

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birth_place = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    religion = db.Column(db.String(20), nullable=False)
    
    # Contact Information
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Academic Information
    previous_school = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(10), unique=True, nullable=False)
    
    # Parent Information
    parent_name = db.Column(db.String(100), nullable=False)
    parent_phone = db.Column(db.String(15), nullable=False)
    parent_occupation = db.Column(db.String(50), nullable=False)
    
    # File Upload Paths
    photo_path = db.Column(db.String(255))
    
    # Status and Timestamps
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.full_name}>'