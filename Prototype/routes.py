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
    return render_template('index.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(user)
            flash("Login successful!!")
            return redirect(url_for('vote'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
            user = Users(email=form.email.data, PwdHash=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return flash("Unknown error please try again later")
    return render_template('register.html', title="Online Vote - Register",form=form)

@app.route("/vote", methods=['GET','POST'])
def vote():
    if current_user.is_authenticated:
        if current_user.check_vote_eligibility():
            form = SubmitVoteForm()
            form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
            parties = PoliticalParty.query.all()
            if request.method == 'POST':
                flash("Thank you for voting " + form.chosenParty.data)
                return redirect(url_for('login'))
            return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)
        else:
            return redirect(url_for('unauthorised'))
    else:
        flash("Please login to access this page")
        return redirect(url_for('login'))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = loginForm()
    if request.method == 'POST':
        admin = Officials.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(admin)
            flash("Login successful!!")
            return redirect(url_for('adminHome'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('admin'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")
