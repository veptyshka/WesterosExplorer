from flask import Flask, render_template, redirect, url_for, flash
from models import db, House, Seat, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm

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


# Registration route
@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account was succesfully created! You can login now', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form = form)

# Login route
@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validete_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login error. Please check your email and apssword', 'danger')

    return render_template('login.html', form = form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

with app.app_context():
    if House.query.count() == 0: # Check if there are houses in the database
        houses_data = [
            {"name": "Stark", "lands": "The North", "description": "Winter is Coming", "emblem": "House_Stark.png", "seat": {"name": "Winterfell", "location": ""}},
            {"name": "Lannister", "lands": "The West", "description": "Hear me Roar!", "emblem": "House_Lannister.png", "seat": {"name": "Casterly Rock", "location": ""}},
            {"name": "Baratheon", "lands": "Stormlands", "description": "Ours is the Fury", "emblem": "House_Baratheon.png", "seat": {"name": "Storm's End", "location": ""}},
            {"name": "Targaryen", "lands": "Crownlands", "description": "Fire and Blood", "emblem": "House_Targaryen.png", "seat": {"name": "Dragonstone", "location": ""}},
            {"name": "Greyjoy", "lands": "Iron Islands", "description": "We Do Not Sow", "emblem": "House_Greyjoy.png", "seat": {"name": "Pyke", "location": ""}},
            {"name": "Tully", "lands": "Riverlands", "description": "Family, Duty, Honor", "emblem": "House_Tully.png", "seat": {"name": "Riverrun", "location": ""}},
            {"name": "Arryn", "lands": "Vale of Arryn", "description": "As High as Honot", "emblem": "House_Arryn.png", "seat": {"name": "Eyrie", "location": ""}},
            {"name": "Tyrell", "lands": "Reach", "description": "Growing Strong", "emblem": "House_Tyrell.png", "seat": {"name": "Highgarden", "location": ""}},
            {"name": "Martell", "lands": "Dorne", "description": "Unbowed, Unbent, Unbroken", "emblem": "House_Martell.png", "seat": {"name": "Солнечное Копьё", "location": ""}},
            {"name": "Night's Watch", "lands": "The Wall", "description": "", "emblem": "Night's_Watch.png", "seat": {"name": "Castle Black", "location": ""}},
        ]

        for house_data in houses_data:
            house = House(name = house_data["name"], lands = house_data["lands"], description = house_data["description"], emblem = house_data["emblem"], )
            db.session.add(house)
            db.session.flush() # to get house id before adding it's seat

            seat_data = house_data["seat"]
            seat = Seat(name = seat_data["name"], location = seat_data["location"], house_id = house.id)
            db.session.add(seat)

        db.session.commit()