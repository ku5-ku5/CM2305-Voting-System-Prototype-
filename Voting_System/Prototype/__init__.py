from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'de7f35de261b964a421d1f296a151bf76ecffe5207861827'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PASSWORD@localhost:3306/votedb'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'vote.prototype@gmail.com',
    "MAIL_PASSWORD": 'xkazmyfdWDyXJ9p'
}

mail = Mail(app)

from Prototype import routes
