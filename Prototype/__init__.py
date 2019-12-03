from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '27a695e8e5c505c88f6de409f873e7a06543dca3c40c9cbb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Belgium2015@localhost:3306/votedb'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from Prototype import routes
