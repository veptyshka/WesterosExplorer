from flask import Blueprint, session, render_template, redirect, url_for, flash
from functools import wraps
from models import db
from models.models import UserRole, User, House

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("You must be logged in to go there", "danger")
            return redirect(url_for("auth.login"))
        
        user = User.query.get(user_id)
        if user.role != UserRole.ADMIN:
            flash("You do not have permission to access the Heart tree", "danger")
            return redirect(url_for("main.home"))
        
        return f(*args, **kwargs)
    return decorated_function


# Heart tree (admin dashboard)
@admin.route("/admin")
@admin_required
def admin_dashboard():
    users = User.query.all()
    houses = House.query.all()
    return render_template("admin_dashboard.html", users = users, houses = houses)
    # flash("Welcome back, Three-eyed crow!")

# Set house leader
@admin.route("/set_leader/<int:user_id>/<int:house_id>")
@admin_required
def set_leader(user_id, house_id):
    user = User.query.get(user_id)
    house = House.query.get(house_id)

    if user and house:
        user.house_id = house.id
        user.role = UserRole.HOUSE_LEADER
        db.session.commit()
        flash(f"{user.username} is now the leader of house {house.name}!", "success")
    else:
        flash("User or house not found", "danger")

    return redirect(url_for("admin.admin_dashboard"))

# Delete user
@admin.route("/delete_user/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} has been banished from Westeros", "success")
    return redirect(url_for("admin.admin_dashboard"))