from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
	first_name = StringField('first name', [validators.Length(min=1)])
	last_name = StringField('last name', [validators.Length(min=1)])
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class DeleteForm(FlaskForm):
	pass
