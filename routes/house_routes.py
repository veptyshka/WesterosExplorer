from flask import Blueprint, render_template, abort, jsonify
from sqlalchemy.orm import joinedload
from models import db
from models.models import House, User

house_bp = Blueprint('house', __name__)

@house_bp.route("/house/<house_name>")
def house_page(house_name):

    # Checking for house in database
    house = House.query.filter_by(name = house_name).first_or_404()
    members = User.query.filter_by(house_id = house.id).all()

    if not house:
        abort(404) # No house found

    return render_template("house_page.html", house = house, members = members, seat = house.seat)

@house_bp.route("/api/castles")
def get_castles():
    houses = House.query.options(db.joinedload(House.seat)).all()

    castles = []
    for house in houses:
        if not house.seat:
            continue

        try:
            x, y = map(int, house.seat.location.split(','))
        except (AttributeError, ValueError):
            continue

        castles.append({
            'id': house.id,
            'name': house.seat.name,
            'house': house.name,
            'x': x,
            'y': y,
            'emblem': house.emblem,
            'words': house.words
        })
    return jsonify(castles)