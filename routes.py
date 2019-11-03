import os
from flask import render_template, url_for, request, redirect, flash
from prototype import app

@app.route("/")
@app.route("/vote")
def vote():
	return(render_template('vote.html'))