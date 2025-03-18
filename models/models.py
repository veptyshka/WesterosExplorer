from flask_login import UserMixin
from models.__init__ import db
from models import bcrypt

class House(db.Model):
    id = db.Column(db.Integer, primary_key = True) # House id
    name = db.Column(db.String(100), unique = True, nullable = False) # House name
    seat = db.relationship("Seat", uselist = False, back_populates = "house") # House seat - family castle
    lands = db.Column(db.String(100), unique = True, nullable = False) # House lands
    words = db.Column(db.Text, nullable = False)
    emblem = db.Column(db.String(255)) # Coat of Arms
    users = db.relationship("User", backref = "house", lazy = True) # Users joined the house


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    avatar = db.Column(db.String(255), nullable = False, default = "default_avatar.png")
    status = db.Column(db.String(255), nullable = True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable = True)
    house = db.relationship('House', backref = db.backref('members', lazy = True))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') # Password hash encryption

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    location = db.Column(db.String(255), nullable = False) # Castle location on the map
    house_id = db.Column(db.Integer, db.ForeignKey('house_id'), unique = True, nullable = False)
    house = db.relationship("House", back_populates = "seat") # House that castle belongs to