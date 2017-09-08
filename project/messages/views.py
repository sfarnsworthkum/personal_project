from flask import Blueprint, redirect, url_for, render_template, request
from project.messages.models import Message
from project import db
from project.messages.forms import MessageForm, DeleteForm
from project.users.models import User

messages_blueprint = Blueprint(
	'messages',
	__name__,
	template_folder='templates'
	)

@messages_blueprint.route('/users/<int:user_id>/messages', methods= ["GET", "POST"])
def message_index(user_id):
	user = User.query.get(user_id)
	form = MessageForm(request.form)
	if request.method == "POST":
		if form.validate():
			new_message = Message(request.form.get("text"), user_id)
			db.session.add(new_message)
			db.session.commit()
		return redirect(url_for("messages.message_index", user_id=user_id))
	return render_template("messages/index.html", user=user, form=form)

@messages_blueprint.route('/users/<int:user_id>/messages/new')
def new_message(user_id):
	user= User.query.get(user_id)
	form=MessageForm()
	return render_template("messages/new.html", user=user, form=form)

@messages_blueprint.route('/users/<int:user_id>/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show_message(user_id, id):
	message = Message.query.get(id)
	form = MessageForm(request.form)
	user = User.query.get(user_id)
	delete_form = DeleteForm(request.form)
	if request.method == b"PATCH":
		if form.validate():
			message.text = request.form.get("text")
			db.session.add(message)
			db.session.commit()
			return redirect(url_for("messages.message_index", user_id=message.user_id))
		else:
			return render_template("messages/edit.html",user=user, message=message, form=form)
	if request.method == b"DELETE":
		if delete_form.validate():
			db.session.delete(message)
			db.session.commit()
			return redirect(url_for("messages.message_index", user_id=message.user_id))
	return render_template("messages/show.html", message=message, form=form, delete_form=delete_form, user=user)

@messages_blueprint.route('/users/<int:user_id>/messages/<int:id>/edit',methods=["GET"])
def edit_message(user_id, id):
	user = User.query.get(user_id)
	message= Message.query.get(id)
	form = MessageForm(obj=message)
	delete_form = DeleteForm(request.form)
	return render_template("messages/edit.html", user=user, message=message, form=form, delete_form=delete_form)
