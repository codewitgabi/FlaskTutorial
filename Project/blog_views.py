from .blueprint import blog, bp
from flask import request, session, url_for, render_template, g, redirect
from .db import get_db
from .decorators import login_required
from markupsafe import escape

@blog.route("/")
@login_required
def home():
	""" List View """
	print(session.get("user_id"))
	posts = get_db().execute("""
		SELECT * FROM post
	""").fetchall()
	posts = [post for post in posts]
	return render_template("blog/index.html", posts=posts)
	
	
@blog.route("/create/", methods=["POST", "GET"])
def create_post():
	""" Create View """
	if request.method == "POST":
		title = request.form.get("title")
		body = request.form.get("body")
		
		db = get_db()
		db.execute("INSERT INTO post (title, content, author_id) VALUES (?, ?, ?)", (title, body, g.user["id"]))
		db.commit()
		
		return redirect(url_for("blog.home"))
		
	return render_template("blog/create-post.html")
	
	
@blog.route("/post/<int:id>/")
def get_post(id):
	""" Retrieve View """
	post = get_db().execute("SELECT title, content  FROM post WHERE id = ?", (escape(id),)).fetchone()
	
	return render_template("blog/post.html", post=post)
	
	
@blog.route("/post/delete/<int:id>/")
def del_post(id):
	""" Delete View """
	db = get_db()
	db.execute("DELETE FROM post WHERE id = ?", (escape(id),))
	db.commit()
	return redirect(url_for("blog.home"))