import os
from flask import render_template, url_for, request, redirect, flash
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
from Prototype import app, db
from Prototype.forms import loginForm, registrationForm, SubmitVoteForm
from Prototype.models import Users, PoliticalParty, Vote, Officials

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        user_pw_hash = Users.query.filter_by(email=form.email.data).options(load_only("PwdHash"))
        if user is not None and check_password_hash(user_pw_hash, form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for('vote'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))
    return render_template('login.html', title="Online Vote - Login",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data, "sha256")
        if check_password_hash(password_hash, form.password.data):
            user = Users(email=form.email.data, PwdHash=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return flash("Password error please try again")
    return render_template('register.html', title="Online Vote - Register",form=form)

@app.route("/vote", methods=['GET','POST'])
def vote():
    form = SubmitVoteForm()
    form.chosenParty.choices = [(PoliticalParty.UId, PoliticalParty.Name) for PoliticalParty in PoliticalParty.query.all()]
    parties = PoliticalParty.query.all()
    if request.method == 'POST':
        flash("Thank you for voting " + form.chosenParty.data)
        return redirect(url_for('login'))
    elif if not current_user.is_authenticated:
        return render_template('unauthorised.html', title="Unauthorised")
    return render_template('vote.html', politicalparty=parties, title="Voting Page", form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = loginForm()
    if request.method == 'POST':
        admin = Officials.query.filter_by(email=form.email.data).first()
        official_pw_hash = Officials.query.filter_by(email=form.email.data).options(load_only("PwdHash"))
        if admin is not None and check_password_hash(official_pw_hash, form.password.data):
            login_user(admin)
            flash("Login successful!!")
            return redirect(url_for('adminHome'))
        elif current_user is not admin:
            return render template('unauthorised.html', title="Unauthorised")
        else:
            flash("Invalid username or password!")
            return redirect(url_for('admin'))

@app.route("/unauthorised", methods=['GET','POST'])
def unauthorised():
    return render_template('unauthorised.html', title="Unauthorised")

@app.route("/voterhome", methods=['GET', 'POST'])
def voterhome():
    return render_template('voterhome.html', title="Voter Homepage")

