import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, House

user_bp = Blueprint('user', __name__)

UPLOAD_FOLDER = 'static/avatars/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user_profile(username):
    user = User.query.filter_by(username = username).first_or_404()

    if request.method == "POST":
        if "avatar" in request.files:
            file = request.files["avatar"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                user.avatar = filename
                db.session.commit()
                flash("Avatar was successfully updated!", "success")

        if "username" in request.form:
            new_name = request.form["username"]
            if new_name and new_name != user.username:
                user.username = new_name
                db.session.commit()
                flash("Your name was successfully updated!", "success")


        if "status" in request.form:
            new_status = request.form["status"]
            user.status = new_status
            db.session.commit()
            flash("Status updated!", "success")

        return redirect(url_for("user.user_profile", username = user.username))
    
    return render_template("user_profile.html", user = user)