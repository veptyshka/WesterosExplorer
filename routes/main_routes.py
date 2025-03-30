from flask import Blueprint, render_template
from flask_login import login_required
from models.models import UserRole

main = Blueprint('main', __name__)

# Homepage
@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html", UserRole=UserRole)

# Map
@main.route("/map")
@login_required # Only for registered users
def map():
    return render_template("map.html")

# Credits
@main.route("/credits")
def credits():
    return render_template("credits.html")