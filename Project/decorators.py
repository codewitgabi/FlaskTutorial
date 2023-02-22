import functools
from flask import g, redirect, url_for

def login_required(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if g.user is None:
			return redirect(url_for("auth.login"))
		return func(*args, **kwargs)
	return wrapper
	