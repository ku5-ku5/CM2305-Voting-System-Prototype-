from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a8c2ba043e7b74aa0da7d2c0009effb8f6f9b0c36c45eab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Belgium2015@localhost:3306/votedb'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from votingsystem import routes
