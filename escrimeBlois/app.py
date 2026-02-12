from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
mail = Mail(app)

@app.context_processor
def inject_form():
    """Inject the contact form into all templates"""
    from .form import FormFormulaire
    return dict(form=FormFormulaire())
