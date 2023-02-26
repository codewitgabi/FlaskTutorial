from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "naba62hs-kwow7wve"

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	
	
with app.app_context():
	db.create_all()

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	if request.method == "POST":
		username = request.form.get("name")
		password = request.form.get("password")
		
		users = db.session.execute(db.select(User)).scalars().all()
		if any([username == user.username for user in users]):
			flash("User with username already exists")
		else:
			if len(password) < 8:
				flash("Minimum length of 8 characters is required.")
			else:
				user = User(
					username=username,
					password=password
				)
				db.session.add(user)
				db.session.commit()
			
			return redirect(url_for("signup"))
		
	return render_template("signup.html")
	
	
if __name__ == "__main__":
	app.run(port=5000, debug=True)