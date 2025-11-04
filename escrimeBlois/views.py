from flask import render_template
from .app import app

@app.route('/')
@app.route('/index/')
def index():
        return render_template("index.html")

@app.route('/login/')
def login():
        return render_template("login.html")
@app.route('/historique/')
def historique():
        return render_template('historique.html')
