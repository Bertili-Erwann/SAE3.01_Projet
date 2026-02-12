import os
try:
    from dotenv import load_dotenv
    # Charger le .env depuis la racine du projet
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path)
except ModuleNotFoundError:
    pass

from .app import app, db
from . import views
import escrimeBlois.commands
import escrimeBlois.models
