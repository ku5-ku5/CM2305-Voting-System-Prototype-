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
    #Renders the template for the officials and admin homepage
    return render_template('officials_home.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    #initiates login form
    form = loginForm()
    if form.validate_on_submit():
        #gets the data from the form
        user = Official.query.filter_by(email=form.email.data).first()
        #checks that the user exists and that the password is correct
        if user is not None and user.verify_password(hashlib.sha256(form.password.data.encode()).hexdigest()):
            #uses the flask login and logs in the user
            login_user(user)
            flash("Login Successful", 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", 'danger')
            return redirect(url_for('login'))
    return render_template('officials_login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
#In a real working system this wouldn't exist
def register():
    #initiates the registration form
    form = Officials_Registration()
    if form.validate_on_submit():
        #gets the data from the form
        #hashes the password in a sha256 hash
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = Official(firstname=form.firstname.data, surname=form.lastname.data, email=form.email.data, password=password_hash)
        #pushes the user data to the database
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('officials_register.html', title="Register as an Official", form=form)

#page for admins to create an election
@app.route("/create_election", methods=['GET', 'POST'])
def create_election():
    #initiates the create election form
    form = CreateElectionForm()
    if form.validate_on_submit():
        #Takes the data from the form and creates the new election as an Election object
        new_election = Election(title=form.title.data, election_date=form.election_date.data, start_time=form.start_time.data, end_time=form.end_time.data)
        #adds the new election to the database
        db.session.add(new_election)
        db.session.commit()
        flash("Successfully Created Election!", "success")
        return redirect(url_for('index'))
    return render_template("create_election.html", title="Create Election", form=form)

#A page for admins and officials to view elections
@app.route('/view_election')
def view_election():
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM election")
    data = cursor.fetchall()
    return render_template('view_election.html', title='View Election', data=data)

@app.route("/logout")
def logout():
    #using flask login user management this page logs out the user
	logout_user()
	return redirect(url_for('index'))

@app.route("/results", methods=['GET', 'POST'])
def results():
    #page that gets all the vote data for the current election
    # votes = Vote.query.all()
    # parties = PoliticalParty.query.all()
    # results = {}
    # for party in parties:
    #     results[party.Name] = 0
    # for vote in votes:
    #     for party in parties:
    #         if vote.PoliticalPartyID == party.UId:
    #             results[party.Name] = results[party.Name] + 1
    #
    #         y_pos = np.arange(len(results.keys()))
    #         plt.bar(y_pos, results.values(), align='center', alpha=0.5)
    #         plt.xticks(y_pos, results.keys())
    #         plt.ylabel('Votes')
    #         plt.title('Election Results')
    #         plt.savefig('Application/static/images/results_plot.png')

            return render_template("results.html", title="Election Results", url="/../static/images/results_plot.png")
