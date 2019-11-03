from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Booleanfield
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SubmitVoteForm(FlaskForm):
	