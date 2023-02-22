from .blueprint import bp
from flask import request, session, redirect, render_template, url_for, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .decorators import login_required


@bp.before_app_request
def load_users():
	user_id = session.get("user_id")
	
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route("/signup/", methods=["GET", "POST"])
@login_required
def signup():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		
		db = get_db()
		error = None
		
		if not username:
			error = "Username field is required"
		elif not password:
			error = "Password field is required"
		elif db.execute(
			"SELECT * FROM user WHERE username = ?", (username,)
		).fetchone() is not None:
			error = "User with this username already exists."
		
		if error is None:
			db.execute(
				"""
				INSERT INTO user (username, password)
				VALUES (?, ?)
				""", (username, generate_password_hash(password)))
			db.commit()
			
			return redirect(url_for("auth.login"))
			
		flash(error)
		
	return render_template("auth/signup.html")


@bp.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		
		db = get_db()
		error = None
		
		user =  db.execute("""
			SELECT * FROM user WHERE username = ? 
		""", (username,)).fetchone()
		
		if not user:
			error = "User with username does not exist"
			
		elif not check_password_hash(user["password"], password):
			error = "Incorrect Password"
		
		if error is None:
			session.clear()
			session["user_id"] = user["id"]
			return redirect(url_for("auth.signup"))
			
		flash(error)
		
	return render_template("auth/signin.html")


@bp.route("/logout/", methods=["GET"])
def logout():
	session.clear()
	return redirect(url_for("auth.signup"))