#/usr/bin/python3

import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Prototype import app, db
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote
from Prototype.email import send_mail
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(Email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(user)
            flash("Login successful!!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if request.method == 'POST':
        if form.validate_on_submit() & (db.session.query(db.session.query(Users).filter_by(Email=form.email.data).exists()).scalar() == False):
            password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
            user_email = form.email.data
            subject = "Registration for online voting " + form.firstName.data
            user = Users(Email=user_email, PwdHash=password_hash)
            db.session.add(user)
            db.session.commit()
            send_mail(user_email, subject, 'Registration_Email\\email.html')
            return redirect(url_for('home'))
        else:
            return flash("Unknown error please try again later")
    return render_template('register.html', title="Online Vote - Register",form=form)

@app.route("/vote", methods=['GET','POST'])
def vote():
    if current_user.is_authenticated:
        if current_user.check_vote_eligibility() & current_user.check_has_voted():
            form = SubmitVoteForm()
            form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
            parties = PoliticalParty.query.all()
            return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)
        if request.method == 'POST':
            vote = form.chosenParty.data
            db.session.add(vote)
            flash("Thank you for voting " + form.chosenParty.data)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('unauthorised'))
    else:
        flash("Please login to access this page")
        return redirect(url_for('login'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")

@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title="User Home Page")
    else:
        return redirect(url_for('unauthorised'))
