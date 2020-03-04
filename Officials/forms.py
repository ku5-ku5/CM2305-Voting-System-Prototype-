from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from Officials.models import Official, Election, Candidates

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

class CreateElectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Please enter the title for the election (e.g. "General Election 2019")')])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Candidates')

    def validate_title(self, title):
        election_title = Election.query.filter_by(title=title.data).first()
        if election_title:
            raise ValidationError('This title is already in use')

class add_candidate_form(FlaskForm):
    title = StringField('Title of Election', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    party = StringField('Party', validators=[DataRequired()])
    submit = SubmitField('Add this Candidates')
