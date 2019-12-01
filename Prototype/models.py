from Prototype import db, login_manager
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.postgresql import UUID

class PoliticalParty(db.Model):
	UId = db.Column(UUID(as_uuid = True), unique = True, primary_key = True)
	Name = db.Column(db.String(255), nullable = False)

	def __repr__(self):
		return f"PoliticalParty('{self.Name}')"

class Users(db.Model):
	UserUId = db.Column(UUID(as_uuid=True), unique = True, primary_key = True)
	EligibleToVote = db.Column(TINYINT(1), default = 0)
	email = db.Column(db.String(255), unique = True, nullable = False)
	PwdHash = db.Column(db.String(255), nullable = False)
	HasVoted = db.Column(TINYINT(1), default = 0)

	def __repr__(self):
		return f"User('{self.EligibleToVote}', '{self.Email}', '{self.PwdHash}')"

class Vote(db.Model):
	VoteId = db.Column(UUID(as_uuid=True), unique = True, primary_key = True)
	PoliticalPartyID = db.Column(db.CHAR(38), db.ForeignKey('party.UId'), nullable = False)
	VoteStatus = db.Column(TINYINT(1), default = 0)
	VoteTimestamp = db.Column(db.DATETIME(), nullable = False)

	def __repr__(self):
		return f"Vote('{self.VoteStatus}')"

class Officials(db.Model):
	OfficialUId = db.Column(UUID(as_uuid=True), unique = True, primary_key = True)
	FirstName = db.Column(db.String(50), nullable=False)
	Surname = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(255), unique = True, nullable = False)
	PwdHash = db.Column(db.String(255), nullable = False)
	HasVoted = db.Column(TINYINT(1), default = 0)
	IsAdmin = db.Column(TINYINT(1), default = 0)

	def __repr__(self):
		return f"User('{self.FirstName}','{self.Surname}', '{self.Email}', '{self.PwdHash}', '{self.IsAdmin}')"
