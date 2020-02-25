
from Officials import db, login_manager
import hashlib
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.postgresql import UUID

@login_manager.user_loader
def load_user(user_id):
	return Official.query.get(int(user_id))

class Official(db.Model, UserMixin):
		id = db.Column(db.Integer, primary_key=True)
		email = db.Column(db.String(120), unique=True, nullable=False)
		password = db.Column(db.String(60), nullable=False)

		def __repr__(self):
			return f"User('{self.email}')"

		def verify_password(self, password):
			return self.password == password
