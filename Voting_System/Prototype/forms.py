from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from Prototype.models import Users

class registrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired('Please enter your first name'), Length(min=3, max=50)])
    surname = StringField('Last Name', validators=[DataRequired('Please enter your last name'), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    passwordVerify = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, Email):
        mail = Users.query.filter_by(Email=Email.data).first()
        if mail:
            raise ValidationError('Sorry, this email is already being used')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    otp_secret = PasswordField('Token', validators=[DataRequired()])
    useremail=StringField('Please Leave Blank *', validators=[Regexp('^$',message="Please hover over textbox for more information")])
    submit = SubmitField('Login')

class Mewngofnodi(FlaskForm):
    email = StringField('eBost', validators=[DataRequired(), Email()])
    password = PasswordField('Cyfrinair', validators=[DataRequired()])
    otp_secret = PasswordField('Token', validators=[DataRequired()])
    useremail=StringField('Gadwech yn wag *', validators=[Regexp('^$',message="Please hover over textbox for more information")])
    submit = SubmitField('Mewngofnodwch')

class SubmitVoteForm(FlaskForm):
    chosenParty = RadioField('Label')
    submit = SubmitField('Submit Vote')

class Cofrestrwch(FlaskForm):
    firstName = StringField('Enw Cyntaf', validators=[DataRequired('Please enter your first name'), Length(min=3, max=50)])
    surname = StringField('Cyfenw', validators=[DataRequired('Please enter your last name'), Length(min=3, max=50)])
    email = StringField('eBost', validators=[DataRequired(), Email()])
    password = PasswordField('Cyfrinair', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    passwordVerify = PasswordField('Cadarnhewch eich gyfrinair', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Cofrestrwch')

    def validate_email(self, Email):
        mail = Users.query.filter_by(Email=Email.data).first()
        if mail:
            raise ValidationError("Mae'r ebost hon yn cael ei ddefnyddio yn barod")

class Pleidleisio(FlaskForm):
    chosenParty = RadioField('Label')
    submit = SubmitField('Pleidleisiwch')
