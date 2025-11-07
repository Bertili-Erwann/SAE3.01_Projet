from flask import flash, redirect, render_template, request, url_for
from .app import app
from escrimeBlois.models import Formulaire

@app.route('/')
@app.route('/index/')
def index():
        return render_template("index.html")

@app.route('/login/')
def login():
        return render_template("login.html")

@app.route('/mdp_oublier_envoyer_code/')
def mdp_oublier_envoyer_code():
        return render_template("mdp_oublier_envoyer_code.html")

@app.route('/mdp_oublier_code/')
def mdp_oublier_code():
        return render_template("mdp_oublier_code.html")

@app.route('/mdp_oublier_confirmer_mdp/', methods=['GET', 'POST'])
def mdp_oublier_confirmer_mdp():
    if request.method == 'POST':
        newpassword = request.form.get('newpassword')
        newpasswordconfirm = request.form.get('newpasswordconfirm')
        
        if newpassword != newpasswordconfirm:
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template('mdp_oublier_confirmer_mdp.html')
        
        # Ici, tu peux ajouter la logique pour mettre à jour le mot de passe en base
        flash("Mot de passe mis à jour avec succès.", "success")
        return redirect(url_for('login'))  # Ou une autre page
    
    return render_template('mdp_oublier_confirmer_mdp.html')

@app.route('/historique/')
def historique():
        return render_template('historique.html')
@app.route('/renseignement/')
def renseignement():
    return render_template("renseignement.html",title = "renseignement")

@app.route('/nav_responsable/')
def nav_resp():
        return render_template('nav_responsable.html')

@app.route('/gestion_formulaire/')
def gest_form():
        lesFormulaires = Formulaire.query.all()
        return render_template('gestion_formulaire.html', formulaires = lesFormulaires)

@app.route('/create_event/')
def create_event():
        return render_template('resp_creation_event.html')
  
@app.route('/consultation_form/<id_formulaire>/')
def consult_form(id_formulaire):
        unForm = Formulaire.query.get(id_formulaire)
        return render_template('consultation_form.html', selectedFormulaire=unForm)
