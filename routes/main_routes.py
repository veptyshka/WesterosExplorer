from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

# Homepage
@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")

# Map
@main.route("/map")
@login_required # Only for registered users
def map():
    return render_template("map.html")