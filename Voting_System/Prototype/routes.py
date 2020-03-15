#/usr/bin/python3

import os
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists, update, table, column, select, insert
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import datetime
import time
from Prototype import app, db, mail, votedb
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import engine

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
@login_required
def vote():
    if current_user.check_vote_eligibility() & current_user.check_has_voted():
        form = SubmitVoteForm()
        form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
        parties = PoliticalParty.query.all()
        if request.method == 'POST':
            timestamp = datetime.datetime.now()
            vote = Vote(PoliticalPartyID=form.chosenParty.data, VoteTimestamp=timestamp)
            db.session.add(vote)
            current_user.user_has_voted()
            db.session.commit()
            return redirect(url_for('vote_confirmed'))
        return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)
    else:
        return redirect(url_for('unauthorised'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', title="User Home Page")

@app.errorhandler(403)
def unauthorised_403(e):
    return render_template('unauthorised.html', title="Unauthorised"), 403

@app.errorhandler(401)
def unauthorised_401(e):
    return render_template('unauthorised.html', title="Unauthorised"), 401

@app.route("/vote_confirmation", methods=['GET', 'POST'])
def vote_confirmed():
    return render_template('vote_confirmation.html', title="Thank you!")