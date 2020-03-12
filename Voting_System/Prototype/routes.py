#/usr/bin/python3

import os
from flask import render_template, url_for, request, redirect, flash, session
from datetime import timedelta
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Prototype import app, db
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote
from flask_login import login_user, current_user, logout_user, login_required
import pyqrcode
import onetimepass
from io import BytesIO

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
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(user)
            flash("You are now Logged In", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid Email or Password. Please try again", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = Users(Email=form.email.data, PwdHash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created, You can now log in", 'success')
        session['email'] = user.Email
        return redirect(url_for('two_factor_setup'))
    return render_template('register.html', title="Register" ,form=form)

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
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title="User Home Page")
    else:
        return redirect(url_for('unauthorised'))

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))