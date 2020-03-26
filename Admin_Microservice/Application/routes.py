import os
from flask import render_template, url_for, request, redirect, flash, session
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Application import app, db

from flask_login import login_user, current_user, logout_user, login_required
from Application.forms import Officials_Registration, loginForm, CreateElectionForm
from Application.models import Official, Election, Candidates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

@app.route("/")
@app.route("/home")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('officials_home.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = Official.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            login_user(user)
            flash("Login Successful", 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", 'danger')
            return redirect(url_for('login'))
    return render_template('officials_login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = Officials_Registration()
    if form.validate_on_submit():
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = Official(email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('officials_register.html', title="Register as an Official", form=form)

@app.route("/create_election", methods=['GET', 'POST'])
def create_election():
    form = CreateElectionForm()
    if form.validate_on_submit():
        new_election = Election(title=form.title.data, candidate1=form.candidate1.data, candidate2=form.candidate2.data, candidate3=form.candidate3.data)
        db.session.add(new_election)
        db.session.commit()
        flash("Successfully Created Election!", "success")
        return redirect(url_for('index'))
    return render_template("create_election.html", title="Create Election", form=form)

@app.route('/view_election')
def view_election():
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM election")
    data = cursor.fetchall()
    return render_template('view_election.html', title='View Election', data=data)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/results", methods=['GET', 'POST'])
def results():
    votes = Vote.query.all()
    parties = PoliticalParty.query.all()
    results = {}
    for party in parties:
        results[party.Name] = 0
    for vote in votes:
        for party in parties:
            if vote.PoliticalPartyID == party.UId:
                results[party.Name] = results[party.Name] + 1

            y_pos = np.arange(len(results.keys()))
            plt.bar(y_pos, results.values(), align='center', alpha=0.5)
            plt.xticks(y_pos, results.keys())
            plt.ylabel('Votes')
            plt.title('Election Results')
            plt.savefig('Application/static/images/results_plot.png')

            return render_template("results.html", title="Election Results", url="/../static/images/results_plot.png")
