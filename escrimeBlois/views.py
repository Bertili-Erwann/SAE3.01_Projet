from flask import render_template
from .app import app

@app.route('/')
@app.route('/index/')
def index():
        return render_template("index.html")
@app.route('/historique/')
def historique():
        return render_template('historique.html')
@app.route('/renseignement/')
def renseignement():
    return render_template("renseignement.html",title = "renseignement")