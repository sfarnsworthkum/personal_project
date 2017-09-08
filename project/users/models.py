from project import db
from project.messages.models import Message
from project import bcrypt

class User(db.Model):
	__tablename__= 'users'

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	username = db.Column(db.Text, unique=True)
	password = db.Column(db.Text)
	messages = db.relationship("Message", backref="user")

	def __init__ (self, first_name, last_name, username, password):
		self.first_name = first_name
		self.last_name = last_name
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

	@classmethod
	def authenticate(cls, username, password):
		found_user = cls.query.filter_by(username = username).first()
		if found_user:
			authenticated_user = bcrypt.check_password_hash(found_user.password, password)
			if authenticated_user:
				return found_user
		return False
