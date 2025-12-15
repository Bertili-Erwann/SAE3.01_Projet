from flask import render_template, request
from .app import app
from escrimeBlois.form import FormInscription


@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/historique/')
def historique():
    return render_template('historique.html')


@app.route('/inscription/', )
def inscription():
    form = FormInscription(request.form)
    return render_template('inscription.html', formInscription=form)


@app.route('/inscription/insert', methods=("POST", ))
def insert_inscription():
    form = FormInscription()
    if form.validate_on_submit():
        form.commit_inscription()

    return render_template('inscription.html', formInscription=form)
