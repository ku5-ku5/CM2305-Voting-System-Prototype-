import os
from flask import render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from prototype import app

@app.route("/")
@app.route("/login")
def login():
	return(render_template('login.html', title="Online Vote - Login"))

@app.route("/register", methods=['GET','POST'])
def register():
	form = registrationForm()
	if form.validate_on_submit():
		password_hash = generate_password_hash(form.password.data, "sha256")
		if check_password_hash(password_hash, form.password.data):
			user = Users(Email=form.email.data, password=password_hash)
		else:
			flash("Password error please try again")
	return(render_template('register.html', title="Online Vote - Register"))

@app.route("/vote", methods=['GET','POST'])
def vote():
	parties = PoliticalParty.query.all()
	return(render_template('vote.html', politicalparty=parties, title="Voting Page"))
