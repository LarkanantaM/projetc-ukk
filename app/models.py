from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
import jwt
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Registration(db.Model):
    __tablename__ = 'registration'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birth_place = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    religion = db.Column(db.String(20), nullable=False)
    
    # Contact Information
    phone = db.Column(db.String(15), nullable=False)
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
    ijazah_path = db.Column(db.String(255))
    
    # Status and Timestamps
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        return f'<Registration {self.full_name}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    
    # Payment Information
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)
    payment_proof = db.Column(db.String(255))
    
    # Status and Notes
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    registration = db.relationship('Registration', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.id}>'