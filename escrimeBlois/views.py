from flask import render_template, request, jsonify
from .app import app
from datetime import datetime
from datetime import date
from escrimeBlois.form import FormInscription

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/historique/')
def historique():
    return render_template('historique.html')

@app.route('/inscription/')
def inscription():
    form = FormInscription(request.form)
    return render_template('inscription.html', formInscription=form)
    

@app.route('/inscription/', methods=("POST", ))
def insert_inscription():
    form = FormInscription()
    if form.validate_on_submit():
        form.commit_inscription()
        
    return render_template('inscription.html', formInscription=form)
