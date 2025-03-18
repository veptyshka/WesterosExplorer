from flask import Blueprint, render_template, abort
from models.models import House

house_bp = Blueprint('house', __name__)

@house_bp.route("/house/<house_name>")
def house_page(house_name):

    # Checking for house in database
    house = House.query.filter_by(name = house_name).first()
    members = house.members

    if not house:
        abort(404) # No house found

    return render_template("house_page.html", house = house)