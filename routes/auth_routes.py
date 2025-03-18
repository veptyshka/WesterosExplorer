from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.models import User
from forms.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


# Registration route
@auth.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account was succesfully created! You can login now', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form = form)

# Login route
@auth.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login error. Please check your email and apssword', 'danger')

    return render_template('login.html', form = form)

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'info')
    return redirect(url_for('main.home'))
