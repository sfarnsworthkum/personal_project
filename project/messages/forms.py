from flask_wtf import FlaskForm
from wtforms import StringField, validators

class MessageForm(FlaskForm):
	text = StringField('Message Body', [validators.Length(min=1)])

class DeleteForm(FlaskForm):
	pass