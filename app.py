from flask import Flask
from models import db, House, Seat
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///westeros.db'
app.config['SECRET_KEY'] = ''

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

with app.app_context():
    if House.query.count() == 0: # Check if there are houses in the database
        # adding houses
        stark = House(name = "Stark", lands = "The North", description = "Winter is coming", emblem = "House_Stark.png")
        baratheon = House(name = "Baratheon", lands = "Stormlands", description = "Ours is the Fury", emblem = "House_Baratheon.png")
        lannister = House(name = "Lannister", lands = "The West", description = "Hear me Roar!", emblem = "House_Lannister.png")
        targaryen = House(name = "Targaryen", lands = "Crownlands", description = "Fire and Blood", emblem = "House_Targaryen.png")
        martell = House(name = "Martell", lands = "Dorne", description = "Unbowed, Unbent, Unbroken", emblem = "House_Martell.png")
        tyrell = House(name = "Tyrell", lands = "Reach", description = "Growing Strong", emblem = "House_Tyrell.png")
        arryn = House(name = "Arryn", lands = "Vale of Arryn", description = "As High as Honor", emblem = "House_Arryn.png")
        tully = House(name = "Tully", lands = "Riverlands", description = "Family, Duty, Honor", emblem = "House_Tully.png")
        greyjoy = House(name = "Greyjoy", lands = "Iron Islands", description = "We Do Not Sow", emblem = "House_Greyjoy.png")
        nights_watch = House(name = "Night's Watch", lands = "The Wall", description = "", emblem = "Night's_Watch.png")
        
        db.session.add(stark)
        db.session.add(baratheon)
        db.session.add(lannister)
        db.session.add(targaryen)
        db.session.add(martell)
        db.session.add(tyrell)
        db.session.add(arryn)
        db.session.add(tully)
        db.session.add(greyjoy)
        db.session.add(nights_watch)
        db.session.commit()

        # adding seats
        winterfell = Seat(name = "Winterfell", location = "", house_id = stark.id)
        storms_end = Seat(name = "Storm's End", location = "", house_id = baratheon.id)
        casterly_rock = Seat(name = "Casterly Rock", location = "", house_id = lannister.id)
        dragonstone = Seat(name = "Dragonstone", location = "", house_id = targaryen.id)
        sunspear = Seat(name = "Sunspear", location = "", house_id = martell.id)
        highgarden = Seat(name = "Highgarden", location = "", house_id = tyrell.id)
        eyrie = Seat(name = "Eyrie", location = "", house_id = arryn.id)
        riverrun = Seat(name = "Riverrun", location = "", house_id = tully.id)
        pyke = Seat(name = "Pyke", location = "", house_id = greyjoy.id)
        castle_black = Seat(name = "Castle Black", location = "", house_id = nights_watch.id)

        db.session.add(winterfell)
        db.session.add(storms_end)
        db.session.add(casterly_rock)
        db.session.add(dragonstone)
        db.session.add(sunspear)
        db.session.add(highgarden)
        db.session.add(eyrie)
        db.session.add(riverrun)
        db.session.add(pyke)
        db.session.add(castle_black)
        db.session.commit()