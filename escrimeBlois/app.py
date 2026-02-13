from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import re
from markupsafe import Markup

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
mail = Mail(app)

def urlify(text):
    """Convertit les URLs en liens cliquables"""
    url_pattern = re.compile(r'(https?://\S+)')
    return Markup(url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text))

app.jinja_env.filters['urlify'] = urlify

@app.context_processor
def inject_form():
    """Inject the contact form into all templates"""
    from .form import FormFormulaire
    return dict(form=FormFormulaire())
