from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another one.')

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    birth_place = StringField('Birth Place', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    religion = SelectField('Religion', choices=[
        ('islam', 'Islam'),
        ('christian', 'Christian'),
        ('catholic', 'Catholic'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('other', 'Other')
    ])
    
    # Contact Information
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    
    # Academic Information
    previous_school = StringField('Previous School', validators=[DataRequired()])
    nisn = StringField('NISN', validators=[DataRequired(), Length(min=10, max=10)])
    
    # Parent Information
    parent_name = StringField('Parent Name', validators=[DataRequired()])
    parent_phone = StringField('Parent Phone', validators=[DataRequired()])
    parent_occupation = StringField('Parent Occupation', validators=[DataRequired()])
    
    submit = SubmitField('Submit Registration')

    def validate_nisn(self, nisn):
        registration = User.query.filter_by(nisn=nisn.data).first()
        if registration:
            raise ValidationError('This NISN is already registered.')