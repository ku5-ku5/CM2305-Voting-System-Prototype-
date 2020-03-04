
#/usr/bin/python3

from Prototype import db, login_manager
import hashlib
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.postgresql import UUID

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
	EligibleToVote = db.Column(TINYINT(1), default = 0)
	Email = db.Column(db.String(255), unique = True, nullable = False)
	PwdHash = db.Column(db.String(255), nullable = False)
	HasVoted = db.Column(TINYINT(1), default = 0)

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
	PoliticalPartyID = db.Column(db.CHAR(38), db.ForeignKey('party.UId'), nullable = False)
	VoteTimestamp = db.Column(db.DATETIME(), nullable = False)

	def __repr__(self):
		return f"Vote('{self.VoteId}', '{self.PoliticalPartyID}', '{self.VoteTimestamp}')"
