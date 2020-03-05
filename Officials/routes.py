import os
from flask import render_template, url_for, request, redirect, flash, session
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Officials import app, db
from flask_login import login_user, current_user, logout_user, login_required
from Officials.forms import Officials_Registration, loginForm, CreateElectionForm
from Officials.models import Official, Election, Candidates


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

# @app.route('/add_candidates', methods=['GET', 'POST'])
# def add_candidates():
#     form = add_candidate_form()
#     if form.validate_on_submit():
#         candidate = Candidates(title=form.title.data, name=form.name.data, party=form.party.data)
#         db.session.add(candidate)
#         db.session.commit()
#         flash("Candidate Added!", "success")
#         return redirect(url_for('add_candidates'))
#     return render_template('add_candidates.html', title='Add Candidates', form=form)

@app.route('/view_election')
def view_election():
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM election")
    data = cursor.fetchall()
    return render_template('view_election.html', title='View Election', data=data)

@app.route('/results')
def results():
    return render_template('results.html', title='Results')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))
