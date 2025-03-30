from flask import Blueprint, session, render_template, redirect, url_for, flash, request
from functools import wraps
from models import db
from models.models import UserRole, User, House
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to go there", "danger")
            return redirect(url_for('auth.login', next=request.url))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != UserRole.ADMIN:
            flash("You do not have permission to access the Heart tree", "danger")
            return redirect(url_for("main.home"))
        
        return f(*args, **kwargs)
    return decorated_function


# Heart tree (admin dashboard)
@admin_bp.route("/")
@admin_required
def dashboard():
    users = User.query.options(joinedload(User.house)).all()
    houses = House.query.options(joinedload(House.seat)).all()
    return render_template("dashboard.html", users = users, houses = houses, UserRole=UserRole)

# Delete user
@admin_bp.route("/users/<int:user_id>/delete", methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.role == UserRole.ADMIN:
        flash("Cannot delete admins", "danger")
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} has been banished from Westeros", "success")

    return redirect(url_for("admin.dashboard"))

# Set house leader
@admin_bp.route("/users/<int:user_id>/set_leader/<int:house_id>", methods=['POST'])
@admin_required
def set_leader(user_id, house_id):
    user = User.query.get_or_404(user_id)
    house = House.query.get(house_id)

    if user.role == UserRole.ADMIN:
        flash("Cannot modify admins", "danger")
    else:
        user.house_id = house.id
        user.role = UserRole.HOUSE_LEADER
        db.session.commit()
        flash(f"{user.username} is now the leader of house {house.name}!", "success")

    return redirect(url_for("admin.dashboard"))