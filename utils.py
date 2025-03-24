from models import db, bcrypt
from models.models import User, UserRole

# Admin creation
def create_admin():
    admin = User.query.filter_by(username = "Three-eyed Raven").first()
    if not admin:
        hashed_password = bcrypt.generate_password_hash("ValarMorghulis")
        admin = User(
            username = "Three-eyed Raven",
            email = "raven@westeros.ws",
            password_hash = hashed_password,
            avatar = "three-eyed_raven.png",
            status = "I see everything...",
            role = UserRole.ADMIN,
            house_id = None,
            house = None
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user 'Three-eyed Raven' created")
    else:
        print("Admin already exists")