from flask import (
	Flask, request,
	session, redirect,
	render_template, url_for)
from markupsafe import escape

# create app instance
app = Flask(__name__)

# set secret key
app.secret_key = b"js6jz2ysh_hsgw72yhwo_916262gakaka"


@app.route("/", methods=["GET"])
def home():
	# check for user authentication
	if not "user" in session:
		return redirect(url_for("login")), 401
		
	return """
			<h1>
				Current User -> %s
			</h1>
			<a href='/logout'>Logout</a>
		""" % escape(session.get("user")), 200


@app.route("/login/", methods=["GET", "POST"])
def login():
	error = ""
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		
		if password == "123":
			app.logger.info("Password is correct")
			session["user"] = username
			return redirect(url_for("home"))
		else:
			error = "Invalid username or password"
		
	return render_template("index.html", error=error)


@app.route("/logout/", methods=["GET"])
def logout():
	session.pop("user")
	return redirect(url_for("login"))