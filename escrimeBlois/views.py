from flask import render_template, request, jsonify
from .app import app
from datetime import datetime


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


@app.route('/date_dynamique', methods=['POST'])
def date_dynamic():
    data = request.get_json()
    date_str = data.get('date_naissance', '')
    if date_str:
        date_user = datetime.strptime(date_str, '%Y-%m-%d').date()
        print("Date récupérée dynamiquement :", date_user)
    return render_template('inscription.html')