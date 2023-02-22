from flask import Blueprint

# works like django's project urls.py include method
bp = Blueprint("auth", __name__, url_prefix="/auth")
blog = Blueprint("blog", __name__)