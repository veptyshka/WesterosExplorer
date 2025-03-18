from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, bcrypt
from models.models import House, Seat, User
from routes.auth_routes import auth
from routes.main_routes import main
from routes.house_routes import house_bp
from routes.user_routes import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///westeros.db'
app.config['SECRET_KEY'] = ''

db.init_app(app)

# Flask login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route register
app.register_blueprint(auth, url_prefix = "/auth")
app.register_blueprint(main, url_prefix = "/")
app.register_blueprint(house_bp)
app.register_blueprint(user_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

with app.app_context():
    if House.query.count() == 0: # Check if there are houses in the database
        houses_data = [
            {"name": "Stark", "lands": "The North", "words": "Winter is Coming", "emblem": "House_Stark.png", "seat": {"name": "Winterfell", "location": "x, y"}},
            {"name": "Lannister", "lands": "The West", "words": "Hear me Roar!", "emblem": "House_Lannister.png", "seat": {"name": "Casterly Rock", "location": "x, y"}},
            {"name": "Baratheon", "lands": "Stormlands", "words": "Ours is the Fury", "emblem": "House_Baratheon.png", "seat": {"name": "Storm's End", "location": "x, y"}},
            {"name": "Targaryen", "lands": "Crownlands", "words": "Fire and Blood", "emblem": "House_Targaryen.png", "seat": {"name": "Dragonstone", "location": "x, y"}},
            {"name": "Greyjoy", "lands": "Iron Islands", "words": "We Do Not Sow", "emblem": "House_Greyjoy.png", "seat": {"name": "Pyke", "location": "x, y"}},
            {"name": "Tully", "lands": "Riverlands", "words": "Family, Duty, Honor", "emblem": "House_Tully.png", "seat": {"name": "Riverrun", "location": "x, y"}},
            {"name": "Arryn", "lands": "Vale of Arryn", "words": "As High as Honot", "emblem": "House_Arryn.png", "seat": {"name": "Eyrie", "location": "x, y"}},
            {"name": "Tyrell", "lands": "Reach", "words": "Growing Strong", "emblem": "House_Tyrell.png", "seat": {"name": "Highgarden", "location": "x, y"}},
            {"name": "Martell", "lands": "Dorne", "words": "Unbowed, Unbent, Unbroken", "emblem": "House_Martell.png", "seat": {"name": "Sunspear", "location": "x, y"}},
            {"name": "Night's Watch", "lands": "The Wall", "words": "", "emblem": "Night's_Watch.png", "seat": {"name": "Castle Black", "location": "x, y"}},
        ]

        for house_data in houses_data:
            house = House(name = house_data["name"], lands = house_data["lands"], words = house_data["words"], emblem = house_data["emblem"], )
            db.session.add(house)
            db.session.flush() # to get house id before adding it's seat

            seat_data = house_data["seat"]
            seat = Seat(name = seat_data["name"], location = seat_data["location"], house_id = house.id)
            db.session.add(seat)

        db.session.commit()