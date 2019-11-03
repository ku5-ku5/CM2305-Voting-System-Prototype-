from prototype import db, login_manager

class PoliticalParty(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	Name = db.Column(db.String(50), nullable = False)

	def __repr__(self):
		return f"PoliticalParty('{self.Name}')"