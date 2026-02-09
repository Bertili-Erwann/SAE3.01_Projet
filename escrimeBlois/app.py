from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
try:
	from dotenv import load_dotenv
	load_dotenv()
except ModuleNotFoundError:
	pass

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
mail = Mail(app)