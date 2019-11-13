import os
from flask import render_template, url_for, request, redirect, flash
from prototype import app

@app.route("/")
@app.route("/login")
def login():
	return(render_template('login.html', title="Online Vote - Login"))

@app.route("/register")
def register():
	return(render_template('register.html', title="Online Vote - Register"))

@app.route("/vote", methods=['GET','POST'])
def vote():
	parties = PoliticalParty.query.all()
	return(render_template('vote.html', politicalparty=parties, title="Voting Page"))
