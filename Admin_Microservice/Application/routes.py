import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Prototype import app, db
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote, Officials
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = loginForm()
    if request.method == 'POST':
        admin = Officials.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(admin)
            flash("Login successful!!")
            return redirect(url_for('admin'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('index'))

@app.route("/admin")
def admin():
    if current_user.is_authenticated:
        if current_user.check_admin_status():
            return render_template("admin.html", title="Admin Home Page")
        else:
            return redirect(url_for('official'))
    else:
        return redirect(url_for('unauthorised'))

@app.route("/official")
def official():
    if current_user.is_authenticated:
        if current_user.check_admin_status() == False:
            return render_template("official.html", title="Officials Home Page")
        elif current_user.check_admin_status():
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('unauthorised'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")
