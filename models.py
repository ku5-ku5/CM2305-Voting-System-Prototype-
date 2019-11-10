from prototype import db, login_manager

class PoliticalParty(db.Model):
	id = db.Column(db.Char(38), primary_key = True)
	Name = db.Column(db.Varchar(255), nullable = False)
	Votes = db.relationship('Vote', backref='party', lazy = True)

	def __repr__(self):
		return f"PoliticalParty('{self.Name}')"

class Users(db.Model):
	id = db.Column(db.Char(38), primary_key = True)
	EligibleToVote = db.Column(db.Binary(1))
	Email = db.Column(db.Varchar(255), nullable = False)
	Password = db.Column(db.Varchar(255), nullable = False)
	IsOfficial = db.Column(db.Binary(1))
	Votes = db.relationship('Vote', backref='user', lazy = True)

	def __repr__(self):
		return f"Users('{self.EligibleToVote}', '{self.Email}', '{self.Password}', '{self.IsOfficial}')"

class Vote(db.Model):
	id = db.Column(db.Char(38), primary_key = True)
	User_id = db.Column(db.Char(38), db.ForeignKey('user.id'), nullable = False)
	Party_id = db.Column(db.Char(38), db.ForeignKey('party.id'), nullable = False)
	VoteStatus = db.Column(db.Binary(1))

	def __repr__(self):
		return f"Vote('{self.VoteStatus}')"

