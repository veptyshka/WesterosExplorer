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
        
        db.session.add(stark)
        db.session.commit()

        # adding seats
        winterfell = Seat(name = "Winterfell", location = "", house_id = stark.id)

        db.session.add(winterfell)
        db.session.commit()