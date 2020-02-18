from datetime import datetime
from votingsystem import db, login_manager
from flask_login import UserMixin
import os
import base64
import onetimepass

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
		id = db.Column(db.Integer, primary_key=True)
		email = db.Column(db.String(120), unique=True, nullable=False)
		password = db.Column(db.String(60), nullable=False)
		otp_secret = db.Column(db.String(16))

		def __init__(self, **kwargs):
			super(User, self).__init__(**kwargs)
			if self.otp_secret is None:
				self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

		def get_totp_uri(self):
			return 'otpauth://totp/Online%20Voting%20System:{0}?secret={1}&issuer=Online%20Voting%20System'.format(self.email, self.otp_secret)

		def verify_totp(self, token):
			return onetimepass.valid_totp(token, self.otp_secret)

		def __repr__(self):
			return f"User('{self.email}')"
