from flask import Flask
from flask_login import LoginManager
from models import db, bcrypt
from models.models import House, Seat, User, UserRole
from routes.auth_routes import auth
from routes.main_routes import main
from routes.house_routes import house_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin
from utils import create_admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///westeros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'rya'

db.init_app(app)
bcrypt.init_app(app)

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
app.register_blueprint(admin)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if there are houses in the database
        houses_exist = House.query.count() > 0
        seats_exist = Seat.query.count() > 0

        if not houses_exist or not seats_exist:
            try:
                print('Adding houses and castles...')

                houses_data = [
                    {"name": "Stark", "lands": "The North", "words": "Winter is Coming", "emblem": "House_Stark.png", "seat": {"name": "Winterfell", "location": "270, 200"}},
                    {"name": "Lannister", "lands": "The West", "words": "Hear me Roar!", "emblem": "House_Lannister.png", "seat": {"name": "Casterly Rock", "location": "150, 505"}},
                    {"name": "Baratheon", "lands": "Stormlands", "words": "Ours is the Fury", "emblem": "House_Baratheon.png", "seat": {"name": "Storm's End", "location": "390, 606"}},
                    {"name": "Targaryen", "lands": "Crownlands", "words": "Fire and Blood", "emblem": "House_Targaryen.png", "seat": {"name": "Dragonstone", "location": "412, 492"}},
                    {"name": "Greyjoy", "lands": "Iron Islands", "words": "We Do Not Sow", "emblem": "House_Greyjoy.png", "seat": {"name": "Pyke", "location": "150, 420"}},
                    {"name": "Tully", "lands": "Riverlands", "words": "Family, Duty, Honor", "emblem": "House_Tully.png", "seat": {"name": "Riverrun", "location": "245, 445"}},
                    {"name": "Arryn", "lands": "Vale of Arryn", "words": "As High as Honor", "emblem": "House_Arryn.png", "seat": {"name": "Eyrie", "location": "355, 415"}},
                    {"name": "Tyrell", "lands": "Reach", "words": "Growing Strong", "emblem": "House_Tyrell.png", "seat": {"name": "Highgarden", "location": "195, 625"}},
                    {"name": "Martell", "lands": "Dorne", "words": "Unbowed, Unbent, Unbroken", "emblem": "House_Martell.png", "seat": {"name": "Sunspear", "location": "415, 735"}},
                    {"name": "Night's Watch", "lands": "The Wall", "words": "Sword in the darkness", "emblem": "Night's_Watch.png", "seat": {"name": "Castle Black", "location": "320, 60"}},
                ]

                for house_data in houses_data:
                    # Checking for a house
                    house = House.query.filter_by(name = house_data["name"]).first()
                    if not house:
                        house = House(
                            name = house_data["name"],
                            lands = house_data["lands"],
                            words = house_data["words"],
                            emblem = house_data["emblem"],
                        )
                        db.session.add(house)
                        print(f"House {house.name} added!")

                    # Checking for a seat
                    seat_data = house_data["seat"]
                    seat = Seat.query.filter_by(name = seat_data["name"]).first()
                    if not seat:
                        seat = Seat(
                            name = seat_data["name"],
                            location = seat_data["location"],
                            house_id = house.id
                        )
                        db.session.add(seat)
                        print(f"Castle {seat.name} for house {house.name} added!")

                db.session.commit()
                print("Successfully created houses and seats")

            except Exception as e:
                db.session.rollback()
                print(f"Error occured: {e}")

        try:
            create_admin()
        
        except Exception as e:
            db.session.rollback()
            print(f"Error occured: {e}")
        app.run(debug = True)