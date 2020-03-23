from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from Application.models import Officials

class registrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired('Please enter your first name'), Length(min=3, max=50)])
    surname = StringField('Last Name', validators=[DataRequired('Please enter your last name'), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    passwordVerify = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, Email):
        mail = Officials.query.filter_by(Email=Email.data).first()
        if mail:
            raise ValidationError('Sorry, this email is already being used')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    useremail=StringField('Please Leave Blank', validators=[Regexp('^$',message="Please hover over textbox for more information")])
    submit = SubmitField('Login')

class SubmitVoteForm(FlaskForm):
    chosenParty = RadioField('Label')
    submit = SubmitField('Submit Vote')

class CreateElectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Please enter the title for the election (e.g. "General Election 2019")')])
    description = StringField('Description', validators=[DataRequired('Please enter a description')])
    startDate = DateField('Start Date', validators=[Regexp('^(0[1-9]|[12][0-9]|3[01])[- /.]'), DataRequired()])
    endDate = DateField('End Date', validators=[Regexp('^(0[1-9]|[12][0-9]|3[01])[- /.]'), DataRequired()])
    submit = SubmitField('Create Election')
