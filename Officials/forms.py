from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class Officials_Registration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('Please enter your first name'), Length(min=3, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired('Please enter your last name'), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validEmail(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('This email is already being used.')
'''
class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    useremail=StringField('Please Leave Blank', validators=[Regexp('^$',message="Please hover over textbox for more information")])
    submit = SubmitField('Login')

class SubmitVoteForm(FlaskForm):
    chosenParty = RadioField('Label')
    submit = SubmitField('Submit Vote')
'''
