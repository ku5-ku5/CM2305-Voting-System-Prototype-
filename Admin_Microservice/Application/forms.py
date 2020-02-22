from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

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
