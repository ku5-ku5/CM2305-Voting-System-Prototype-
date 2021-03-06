from Prototype import db, login_manager#, admin

#/usr/bin/python3

from Prototype import db, login_manager
import hashlib
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.postgresql import UUID
import os
import base64
import onetimepass

class PoliticalParty(db.Model):
	UId = db.Column(UUID(as_uuid = True), unique = True, primary_key = True)
	Name = db.Column(db.String(255), nullable = False)

	def get_id(self):
		try:
			return str(self.UId)
		except AttributeError:
			raise NotImplementedError('No `UId` attribute - override `get_id`')

	def __repr__(self):
		return f"PoliticalParty('{self.Name}')"

class Users(UserMixin, db.Model):
	UserUId = db.Column(UUID(as_uuid=True), unique = True, primary_key = True, default=db.text("uuid()"))
	EligibleToVote = db.Column(TINYINT(1), default = 1)
	Email = db.Column(db.String(255), unique = True, nullable = False)
	PwdHash = db.Column(db.String(255), nullable = False)
	HasVoted = db.Column(TINYINT(1), default = 0)
	otp_secret = db.Column(db.String(16))

	def __init__(self, **kwargs):
			super(Users, self).__init__(**kwargs)
			if self.otp_secret is None:
				self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

	def get_totp_uri(self):
			return 'otpauth://totp/Online%20Voting%20System:{0}?secret={1}&issuer=Online%20Voting%20System'.format(self.Email, self.otp_secret)

	def verify_totp(self, token):
			return onetimepass.valid_totp(token, self.otp_secret)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	def get_id(self):
		try:
			return str(self.UserUId)
		except AttributeError:
			raise NotImplementedError('No `UserUId` attribute - override `get_id`')

	def verify_password(self, password):
		return self.PwdHash == password

	def check_vote_eligibility(self):
		return self.EligibleToVote == 1

	def user_has_voted(self):
		UId = self.UserUId
		return db.engine.execute("update votedb.users set HasVoted = 1 WHERE UserUId = '" + str(UId) + "';")


	#The below returns true if the user hasnt voted
	def check_has_voted(self):
		return self.HasVoted == 0

	@login_manager.user_loader
	def load_user(UserUId):
		return Users.query.get(UserUId)


	def __repr__(self):
		return f"User('{self.EligibleToVote}', '{self.Email}', '{self.PwdHash}')"

class Vote(db.Model):
	VoteId = db.Column(UUID(as_uuid=True), unique = True, primary_key = True, default=db.text("uuid()"))
	PoliticalPartyID = db.Column(db.CHAR(38), db.ForeignKey('political_party.UId'), nullable = False)
	VoteTimestamp = db.Column(db.DATETIME(), nullable = False)

	def __repr__(self):
		return f"Vote('{self.VoteId}', '{self.PoliticalPartyID}', '{self.VoteTimestamp}')"
