import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Application import app, db
from Application.forms import loginForm, CreateElectionForm
from Application.generate_xml import Filename, Generate_xml
from Application.models import Users, PoliticalParty, Officials, Vote
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = loginForm()
    if request.method == 'POST':
        admin = Officials.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(admin)
            flash("Login successful!!")
            return redirect(url_for('admin'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('index'))
    else:
        return render_template("adminLogin.html", form=form, title="Admin Login")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        if current_user.check_admin_status():
            return render_template("admin.html", title="Admin Home Page")
        else:
            return redirect(url_for('official'))
    else:
        return redirect(url_for('unauthorised'))

@app.route("/official", methods=['GET', 'POST'])
def official():
    if current_user.is_authenticated:
        if current_user.check_admin_status() == False:
            return render_template("official.html", title="Officials Home Page")
        elif current_user.check_admin_status():
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('unauthorised'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")

@app.route("/createElection", methods=['GET','POST'])
def createElection():
    form = CreateElectionForm()
    return render_template("election.html", title="Create Election", form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    #if current_user.is_authenticated:
    #    if current_user.check_admin_status() == False:
    votes = Vote.query.all()
    parties = PoliticalParty.query.all()
    results = {}
    vote_total = 0
    for party in parties:
        results[party.Name] = 0
    for vote in votes:
        for party in parties:
            if vote.PoliticalPartyID == party.UId:
                results[party.Name] = results[party.Name] + 1
                vote_total += 1
    return render_template("results.html", title="Election Results", results=results, total=vote_total)
#        elif current_user.check_admin_status():
#            return redirect(url_for('admin'))
#    else:
#        return redirect(url_for('unauthorised'))
