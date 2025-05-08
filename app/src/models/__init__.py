from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.src.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registrations = db.relationship('Registration', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

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
    nisn = db.Column(db.String(10), unique=True, nullable=False)
    
    # Contact Information
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    # School Information
    previous_school = db.Column(db.String(100), nullable=False)
    
    # Parent Information
    parent_name = db.Column(db.String(100), nullable=False)
    parent_phone = db.Column(db.String(15), nullable=False)
    parent_occupation = db.Column(db.String(50), nullable=False)
    
    # Registration Status
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Registration {self.full_name}>'

    def update_status(self, new_status):
        self.status = new_status
        self.processed_at = datetime.utcnow()