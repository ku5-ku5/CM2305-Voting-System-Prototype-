from flask import render_template, url_for, flash, redirect, session
from votingsystem import app, db, bcrypt
from votingsystem.forms import RegistrationForm, LoginForm
from votingsystem.models import User
from flask_login import login_user, current_user, logout_user
from io import BytesIO
import pyqrcode
import onetimepass


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('vote'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your Account has been created. You can now log in!', 'success')
		session['email'] = user.email
		return redirect(url_for('two_factor_setup'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login",  methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('vote'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and user.verify_totp(form.token.data):
			login_user(user)
			return redirect(url_for('vote'))
		else:
			flash('Login Unsuccesful. Please Check email, password and token', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/vote")
def vote():
	return render_template('vote.html', title='Vote')

@app.route("/twofactor")
def two_factor_setup():
	if 'email' not in session:
		return redirect(url_for('home'))
	user = User.query.filter_by(email=session['email']).first()
	if user is None:
		return redirect(url_for('home'))
	return render_template('two-factor-setup.html', title='2FA')

@app.route("/qrcode")
def qrcode():
	if 'email' not in session:
		abort(404)
	user = User.query.filter_by(email=session['email']).first()
	if user is None:
		abort(404)
	del session['email']

	url = pyqrcode.create(user.get_totp_uri())
	stream = BytesIO()
	url.svg(stream, scale=5)
	return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}
