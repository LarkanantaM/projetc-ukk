from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default=UserRole.USER.value)
    status = db.Column(db.String(20), default=UserStatus.PENDING.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with Registration
    registration = db.relationship('Registration', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    registration_number = db.Column(db.String(20), unique=True)
    nisn = db.Column(db.String(20), unique=True)
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    school_origin = db.Column(db.String(100))
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Documents relationship
    documents = db.relationship('Document', backref='registration')

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'))
    document_type = db.Column(db.String(50))  # e.g., 'ijazah', 'kk', 'photo'
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default=UserStatus.PENDING.value)

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(role=UserRole.ADMIN.value).first()
        if not admin:
            admin = User(
                username='admin',
                fullname='Administrator',
                email='admin@ppdb.com',
                role=UserRole.ADMIN.value,
                status=UserStatus.APPROVED.value
            )
            admin.set_password('admin123')  # Change this in production
            db.session.add(admin)
            db.session.commit()