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
    
    # File Upload
    photo = FileField('Photo (3x4)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])