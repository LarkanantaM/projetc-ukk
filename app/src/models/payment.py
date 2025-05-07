from datetime import datetime
from app.src.database import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'), nullable=False)
    
    # Payment Information
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)
    payment_proof = db.Column(db.String(255))  # Path to uploaded proof file
    
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
        return f'<Payment {self.id} for {self.registration.full_name}>'

    @property
    def status_color(self):
        return {
            'pending': 'warning',
            'verified': 'success',
            'rejected': 'danger'
        }.get(self.status, 'secondary')