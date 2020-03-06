#/usr/bin/python3

import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime
from Prototype import app, db, mail
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote

from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/index.html", methods=['GET', 'POST'])
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
            user = Users(Email=user_email, PwdHash=password_hash)
            db.session.add(user)
            db.session.commit()
            msg = Message(subject="Thank You For Registering!",sender='vote.prototype@gmail.com', recipients=user_email)
            msg.html=render_template('\\Registration_Email\\email.html')
            msg.body=msg.html
            mail.send(msg)
        return redirect(url_for('home'))
    return render_template('register.html', title="Online Vote - Register",form=form)

@app.route("/vote", methods=['GET','POST'])
def vote():
    if current_user.is_authenticated:
        if current_user.check_vote_eligibility() & current_user.check_has_voted():
            form = SubmitVoteForm()
            form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
            parties = PoliticalParty.query.all()
            return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)
        else:
            return redirect(url_for('unauthorised'))
    elif request.method == 'POST':
        timestamp = datetime.datetime.now()
        political_party = db.session.query(PoliticalParty).filter_by(Name=form.chosenParty.data).first()
        vote = Vote(PoliticalPartyID=political_party.UId, VoteTimestamp=timestamp)
        db.session.add(vote)
        flash("Thank you for voting " + form.chosenParty.data)
        db.session.commit()
        return redirect(url_for('index'))
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
