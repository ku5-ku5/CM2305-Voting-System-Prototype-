"""
import os
from flask import render_template, url_for, request, redirect, flash
from Prototype import app

@app.route("/")
@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = loginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(Url_for('vote'))
	return(render_template('login.html', title="Online Vote - Login"))

@app.route("/register", methods = ['GET', 'POST'])
def register():
	form = registrationForm()
	if request.method == 'POST':
		user = User(firstName=form.firstName.data, surname=form.surname.data, email=form.email.data, password=form.password.data)
		db.session.add(User)
		db.session.commit()
	return(render_template('register.html', title="Online Vote - Register"))

@app.route("/vote", methods=['GET','POST'])
def vote():
	parties = PoliticalParty.query.all()
	return(render_template('vote.html', politicalparty=parties, title="Voting Page"))
"""
