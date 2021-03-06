from Application import db, login_manager
import hashlib
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.postgresql import UUID

@login_manager.user_loader
def load_user(user_id):
	return Official.query.get(int(user_id))

class Official(db.Model, UserMixin):
	officialuid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(50), nullable=False)
	surname = db.Column(db.String(50),nullable=False)
	email = db.Column(db.String(240), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)


	def get_id(self):
		try:
			return str(self.officialuid)
		except AttributeError:
			raise NotImplementedError('No `UId` attribute - override `get_id`')

	def __repr__(self):
		return f"User('{self.email}')"

	def verify_password(self, password):
		return self.password == password

class Election(db.Model, UserMixin):
	title = db.Column(db.String(255), nullable=False, primary_key=True)
	election_date = db.Column(db.DATE, nullable=False)
	start_time = db.Column(db.TIME, nullable=False)
	end_time = db.Column(db.TIME, nullable=False)

class Candidates(db.Model, UserMixin):
	title = db.Column(db.String(60), primary_key=True)
