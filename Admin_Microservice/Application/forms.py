from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    useremail=StringField('Please Leave Blank', validators=[Regexp('^$',message="Please hover over textbox for more information")])
    submit = SubmitField('Login')

class SubmitVoteForm(FlaskForm):
    chosenParty = RadioField('Label')
    submit = SubmitField('Submit Vote')
