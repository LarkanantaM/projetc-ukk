from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class PaymentForm(FlaskForm):
    amount = DecimalField('Payment Amount', validators=[DataRequired()])
    payment_proof = FileField('Payment Proof', 
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDF only!')
        ])
    notes = StringField('Payment Notes')
    submit = SubmitField('Submit Payment')