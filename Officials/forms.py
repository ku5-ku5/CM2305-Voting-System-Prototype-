from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from Officials.models import Official

class Officials_Registration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        mail = Official.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('This email is already being used.')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
