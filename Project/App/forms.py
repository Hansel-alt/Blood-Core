from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, Length
from wtforms.fields.html5 import EmailField, DateField
from email_validator import validate_email
from datetime import datetime

class SignUp(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    dob = DateField('Date of Birth', format='%d/%m/%Y', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)])
    email = EmailField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=7, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up', render_kw={'class': 'btn w3-indigo waves-effect waves-red white-text'})

class LogIn(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login', render_kw={'class': 'btn w3-indigo waves-effect waves-red white-text'})
