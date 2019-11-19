import os
from flask import render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from Prototype import app
from Prototype.forms import loginForm, registrationForm
from Prototype.models import Users, PoliticalParty, Vote

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        user_pw_hash = Users.query.filter_by(email=form.email.data).options(load_only(PwdHash))
        if user is not None and check_password_hash(user_pw_hash, form.password.data):
            login_user(user)
            flash("Login successful!!")
            return redirect(url_for('vote'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))
    elif request.method == 'GET':
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
    parties = PoliticalParty.query.all()
    return render_template('vote.html', politicalparty=parties, title="Voting Page")
