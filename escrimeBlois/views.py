from flask import render_template, request, jsonify
from .app import app
from datetime import datetime
from datetime import date


@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/historique/')
def historique():
    return render_template('historique.html')


@app.route('/inscription/')
def inscription():
    return render_template('inscription.html')
