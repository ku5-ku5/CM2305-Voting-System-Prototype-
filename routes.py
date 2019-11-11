import os
from flask import render_template, url_for, request, redirect, flash
from prototype import app

@app.route("/")
@app.route("/login")
def login():
	return(render_template('login.html'))

@app.route("/register")
def register():
	return(render_template('register.html'))
	
@app.route("/vote")
def vote():
	return(render_template('vote.html'))