from Prototype import db, login_manager

class PoliticalParty(db.Model):
	UId = db.Column(db.Char(38), unique = True, primary_key = True)
	Name = db.Column(db.Varchar(255), nullable = False)

	def __repr__(self):
		return f"PoliticalParty('{self.Name}')"

class Users(db.Model):
	UId = db.Column(db.Char(38), unique = True, primary_key = True)
	EligibleToVote = db.Column(db.TINYINT(1), default = 0)
	Email = db.Column(db.Varchar(255), unique = True, nullable = False)
	PwdHash = db.Column(db.Varchar(255), nullable = False)
	HasVoted = db.Column(db.TINYINT(1), default = 0)
	IsOfficial = db.Column(db.TINYINT(1), default = 0)
	Votes = db.relationship('Vote', backref='user', lazy = True)

	def __repr__(self):
		return f"User('{self.EligibleToVote}', '{self.Email}', '{self.Password}', '{self.IsOfficial}')"

class Vote(db.Model):
	VoteId = db.Column(db.Char(38), unique = True, primary_key = True)
	PoliticalPartyID = db.Column(db.Char(38), db.ForeignKey('party.UId'), nullable = False)
	VoteStatus = db.Column(db.TINYINT(1))
	VoteTimestamp = db.Column(db.DATETIME(), nullable = False)

	def __repr__(self):
		return f"Vote('{self.VoteStatus}')"
