from flask import Blueprint, request, redirect, url_for, render_template
from project.users.models import User
from project.users.forms import UserForm, DeleteForm
from project import db

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
	'users',
	__name__,
	template_folder='templates'
)

@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
	form = UserForm()
	if request.method == "POST" and form.validate():
		try:
			new_user = User(form.data['username'], form.data['password'])
			db.session.add(new_user)
			db.session.commit()
		except IntegrityError as e:
			render_template('signup.html', form=form)
			return redirect(url_for('users.login'))
	from IPython import embed; embed()
	return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        if User.authenticate(form.data['username'], form.data['password']):
                return redirect(url_for('users.welcome'))
    return render_template('users/login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('users/welcome.html')

@users_blueprint.route('/', methods=["GET","POST"])
def index():
	if request.method == "POST":
		form = UserForm(request.form)
		if form.validate():
			new_user = User(request.form.get("first_name"), request.form.get("last_name"), request.form.get("username"), request.form.get("password"))
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for("users.index"))
		else:
			return render_template("users/new.html", form=form)
	all_users = User.query.all()
	return render_template("users/index.html", users=all_users)



@users_blueprint.route('/new')
def new():
	form = UserForm()
	return render_template('users/new.html', form=form)

@users_blueprint.route('/users/<int:id>', methods = ["GET", "PATCH", "DELETE"])
def show(id):
	form = UserForm(request.form)
	user = User.query.get(id)
	delete_form = DeleteForm(request.form)
	if request.method == b"PATCH":
		if form.validate():
			user.first_name = request.form.get("first_name")
			user.last_name = request.form.get("last_name")
			db.session.add(user)
			db.session.commit()
			return redirect(url_for("users.index"))
		else:
			return render_template("users/edit.html", user=user, form=form)
	if request.method == b"DELETE":
		if delete_form.validate():
			db.session.delete(user)
			db.session.commit()
			return redirect(url_for("users.index"))
	return render_template("users/show.html", user=user, delete_form=delete_form)

@users_blueprint.route('/users/<int:id>/edit', methods = ["GET"])
def edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)
    delete_form = DeleteForm(request.form)
    return render_template("users/edit.html", user=user, form=form, delete_form=delete_form)
