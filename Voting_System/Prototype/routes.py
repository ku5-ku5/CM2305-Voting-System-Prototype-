#/usr/bin/python3

import os
from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_required
from datetime import timedelta
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists, update, table, column, select, insert
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import datetime
import time
from Prototype import app, db, mail, votedb
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm, Mewngofnodi, Cofrestrwch, Pleidleisio
from Prototype.models import Users, PoliticalParty, Vote
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import engine
import pyqrcode
import onetimepass
from io import BytesIO
from werkzeug import abort

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(Email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()) and user.verify_totp(form.otp_secret.data):
            login_user(user)
            flash("You are now Logged In", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid Email, Password or token. Please try again", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if request.method == 'POST':
        if form.validate_on_submit()& (db.session.query(db.session.query(Users).filter_by(Email=form.email.data).exists()).scalar() == False):
            hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
            user = Users(Email=form.email.data, PwdHash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account Created, Please Scan the QR code to recieve your One Time Password", 'success')
            session['email'] = user.Email
            return redirect(url_for('two_factor_setup'))
    return render_template('register.html', title="Register" ,form=form)


@app.route("/vote", methods=['GET','POST'])
@login_required
def vote():
    if current_user.check_vote_eligibility() & current_user.check_has_voted():
        form = SubmitVoteForm()
        #generates a form based on the political parties in the political party table
        form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
        parties = PoliticalParty.query.all()
        if request.method == 'POST':
            timestamp = datetime.datetime.now()
            #creates vote object with the users choice of political party
            vote = Vote(PoliticalPartyID=form.chosenParty.data, VoteTimestamp=timestamp)
            db.session.add(vote)
            #executes a custom sql statement to make the user HasVoted column = 1
            current_user.user_has_voted()
            db.session.commit()
            return redirect(url_for('vote_confirmed'))
        return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)
    elif current_user.check_vote_eligibility() == False:
        return redirect(url_for('unauthorised'))
    elif current_user.check_has_voted() == False:
        return redirect(url_for('alreadyvoted'))

#USERS ARE REDIRECTED TO 2FA PAGE WHEN THEY REGISTER
@app.route("/twofactor")
def two_factor_setup():
	if 'email' not in session:
		return redirect(url_for('index'))
	user = Users.query.filter_by(Email=session['email']).first()
	if user is None:
		return redirect(url_for('index'))
	return render_template('two-factor-setup.html', title='2FA')

#THIS GENERATES THE QR CODE FOR THE 2FA
@app.route("/qrcode")
def qrcode():
	if 'email' not in session:
		abort(404)
	user = Users.query.filter_by(Email=session['email']).first()
	if user is None:
		abort(404)
	del session['email']

	url = pyqrcode.create(user.get_totp_uri())
	stream = BytesIO()
	url.svg(stream, scale=5)
	return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

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

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/alreadyvoted', methods=['GET', 'POST'])
def alreadyvoted():
    return render_template('already_voted.html', title='Already Voted')


#####CYMRAEG########
@app.route('/cartref')
def cartref():
    return render_template('cartref.html', title='cartref')

@app.route("/mewngofnodi", methods=['GET', 'POST'])
def mewngofnodi():
    form = Mewngofnodi()
    if request.method == 'POST':
        user = Users.query.filter_by(Email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()) and user.verify_totp(form.otp_secret.data):
            login_user(user)
            flash("Rydych wedi mewngofnodi yn lwyddianus!", "success")
            return redirect(url_for('cartref'))
        else:
            flash("Ebost, Token neu chyfrinair anghywir", "danger")
            return redirect(url_for('mewngofnodi'))
    return render_template('mewngofnodi.html', title="Mewngofnodwch",form=form)

@app.route("/cofrestrwch", methods=['GET','POST'])
def cofrestrwch():
    form = Cofrestrwch()
    if request.method == 'POST':
        if form.validate_on_submit()& (db.session.query(db.session.query(Users).filter_by(Email=form.email.data).exists()).scalar() == False):
            hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
            user = Users(Email=form.email.data, PwdHash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Cyfrif wedi ei greu, Sganiwch y cod QR i dderbyn eich cyfrinair gyfinachol", 'success')
            session['email'] = user.Email
            return redirect(url_for('dilysu_dau_ffactor'))
    return render_template('cofrestrwch.html', title="Cofrestrwch" ,form=form)

@app.route("/dwyffactor")
def dilysu_dau_ffactor():
	if 'email' not in session:
		return redirect(url_for('cartref'))
	user = Users.query.filter_by(Email=session['email']).first()
	if user is None:
		return redirect(url_for('cartref'))
	return render_template('dilysu_dau_ffactor.html', title='2FA')

@app.route("/Pleidleisiwch", methods=['GET','POST'])
@login_required
def Pleidleisiwch():
    if current_user.check_vote_eligibility() & current_user.check_has_voted():
        form = Pleidleisio()
        #generates a form based on the political parties in the political party table
        form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
        parties = PoliticalParty.query.all()
        if request.method == 'POST':
            timestamp = datetime.datetime.now()
            #creates vote object with the users choice of political party
            vote = Vote(PoliticalPartyID=form.chosenParty.data, VoteTimestamp=timestamp)
            db.session.add(vote)
            #executes a custom sql statement to make the user HasVoted column = 1
            current_user.user_has_voted()
            db.session.commit()
            return redirect(url_for('diolch'))
        return render_template('pleidleisio.html', politicalparty=parties, title="Tudalen Pleidleisio", form=form)
    elif current_user.check_vote_eligibility() == False:
        return redirect(url_for('hebgofrestru'))
    elif current_user.check_has_voted() == False:
            return redirect(url_for('wedipleidleisio'))

@app.route('/hebgofrestru')
def hebgofrestru():
    return render_template('hebgofrestru.html', title='Heb Gofrestru')

@app.route('/wedipleidleisio')
def wedipleidleisio():
    return render_template('wedipleidleisio.html', title='Wedi Pleidleisio yn Barod')

@app.route("/diolch", methods=['GET', 'POST'])
def diolch():
    return render_template('diolch.html', title="Diolch am Bleidleisio!")
