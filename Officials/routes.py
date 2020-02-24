import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Officials import app, db
from flask_login import login_user, current_user, logout_user, login_required
from Officials.forms import Officials_Registration

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('officials_home.html', title="Online Vote System")
'''
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(user)
            flash("Login successful!!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)
'''
@app.route("/register", methods=['GET','POST'])
def register():
    form = Officials_Registration()
    if request.method == 'POST':
        if form.validate_on_submit():
            password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
            user = Users(email=form.email.data, PwdHash=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return flash("Unknown error please try again later")
    return render_template('officials_register.html', title="Register as an Official", form=form)
