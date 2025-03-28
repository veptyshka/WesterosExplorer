from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.models import User

# Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register now!')

    # Check if the username is valid
    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first():
            raise ValidationError('This username already exists')
        
    # Check if the email already exists
    def validate_email(self, email):
        if User.query.filter_by(email = email.data).first():
            raise ValidationError('Looks like this user is already registered')
        

# Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    submit = SubmitField('Login')