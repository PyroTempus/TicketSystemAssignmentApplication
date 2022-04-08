from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Setting up global variables and required libs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsystem.db'
app.config['SECRET_KEY'] = '9b002187c1b68d74db214c6d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Login manager library and setting up the view page and style of messages to show.
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

from ticketsystem import routes
