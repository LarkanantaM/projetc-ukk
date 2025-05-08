SECRET_KEY = 'your-secret-key-here'  # Change this to a secure key

from app.src.forms.admission_form import AdmissionForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from datetime import date

class AdmissionForm(FlaskForm):
    # Personal Information
    full_name = StringField('Full Name', 
        validators=[DataRequired(), Length(min=3, max=100)])
    birth_date = DateField('Date of Birth', 
        validators=[DataRequired()])
    birth_place = StringField('Place of Birth',
        validators=[DataRequired(), Length(max=100)])
    gender = SelectField('Gender',
        choices=[('M', 'Male'), ('F', 'Female')],
        validators=[DataRequired()])
    religion = SelectField('Religion',
        choices=[
            ('islam', 'Islam'),
            ('christian', 'Christian'),
            ('catholic', 'Catholic'),
            ('hindu', 'Hindu'),
            ('buddha', 'Buddha'),
            ('other', 'Other')
        ],
        validators=[DataRequired()])
    
    # Contact Information
    phone = StringField('Phone Number',
        validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    address = TextAreaField('Address',
        validators=[DataRequired(), Length(max=200)])
    
    # Academic Information
    previous_school = StringField('Previous School',
        validators=[DataRequired(), Length(max=100)])
    nisn = StringField('NISN',
        validators=[DataRequired(), Length(min=10, max=10)])
    
    # Parent Information
    parent_name = StringField('Parent/Guardian Name',
        validators=[DataRequired(), Length(max=100)])
    parent_phone = StringField('Parent/Guardian Phone',
        validators=[DataRequired(), Length(min=10, max=15)])
    parent_occupation = StringField('Parent/Guardian Occupation',
        validators=[DataRequired(), Length(max=50)])
    
    # File Upload
    photo = FileField('Photo (3x4)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    
    ijazah = FileField('Ijazah/School Certificate', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    
    submit = SubmitField('Submit Application')

    def validate_birth_date(self, field):
        if field.data > date.today():
            raise ValidationError('Birth date cannot be in the future')
        
        # Calculate age
        today = date.today()
        age = today.year - field.data.year - \
            ((today.month, today.day) < (field.data.month, field.data.day))
        
        # Check if student is between 12-20 years old
        if age < 12 or age > 20:
            raise ValidationError('Student must be between 12-20 years old')

    def validate_nisn(self, field):
        if not field.data.isdigit():
            raise ValidationError('NISN must contain only numbers')
        if len(field.data) != 10:
            raise ValidationError('NISN must be exactly 10 digits')

    def validate_phone(self, field):
        if not field.data.replace('+', '').isdigit():
            raise ValidationError('Invalid phone number format')
            
    def validate_parent_phone(self, field):
        if not field.data.replace('+', '').isdigit():
            raise ValidationError('Invalid phone number format')