from flask import flash, redirect, render_template, request, url_for
from .app import app, db
from escrimeBlois.models import Formulaire, Inscription, Classer, Evenement, Personne
from sqlalchemy import extract, func

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


@app.route('/event_classement_global/', methods=['GET'])
def event_classment():
                disciplines = request.args.getlist('discipline_classment[]') or request.args.getlist('discipline_classment')
                coops = request.args.getlist('coop_classment[]') or request.args.getlist('coop_classment')
                # keep raw values for template (e.g. 'Homme'/'Femme') so boxes stay checked
                sexes_display = request.args.getlist('sexe_classment[]') or request.args.getlist('sexe_classment') or []
                # map display sexes to stored DB values (Homme->M, Femme->F) for filtering
                db_sexes = []
                for s in sexes_display:
                        if s and s.lower().startswith('h'):
                                db_sexes.append('M')
                        elif s and s.lower().startswith('f'):
                                db_sexes.append('F')

                categorie = request.args.get("categorie_event")
                saison = request.args.get("saison_event")
                niveau = request.args.get("niveau_event")

                if categorie in (None, '', 'Toutes'):
                        categorie = None
                if niveau in (None, '', 'Tous'):
                        niveau = None

                events_q = db.session.query(Evenement.id_evenement)
                events_q = events_q.join(Inscription, Inscription.id_evenement == Evenement.id_evenement)

                if disciplines != []:
                        events_q = events_q.filter(Evenement.discipline.in_(disciplines))
                if coops != []:
                        events_q = events_q.filter(Evenement.cooperative.in_(coops))
                if niveau:
                        events_q = events_q.filter(Evenement.niveau == niveau)
                if categorie:
                        events_q = events_q.filter(Evenement.categorie == categorie)
                if saison:
                        try:
                                year = int(saison)
                                events_q = events_q.filter(extract('year', Evenement.date) == year)
                        except ValueError:
                                pass
                if db_sexes != []:
                        events_q = events_q.join(Personne, (Personne.nom_personne == Inscription.nom_inscrit) & (Personne.prenom_personne == Inscription.prenom_inscrit))
                        events_q = events_q.filter(Personne.sexe.in_(db_sexes))

                events_q = events_q.distinct()
                event_rows = events_q.all()
                event_ids = [er.id_evenement for er in event_rows]
                event_count = len(event_ids)

                lesInscrits = []
                if event_count == 0:
                        lesInscrits = []
                else:
                        q = db.session.query(
                                Inscription.nom_inscrit.label('nom_inscrit'),
                                Inscription.prenom_inscrit.label('prenom_inscrit'),
                                func.coalesce(func.sum(Classer.points), 0).label('points')
                        )
                        q = q.join(Classer, Classer.id_competition == Inscription.id_inscription)
                        q = q.filter(Inscription.id_evenement.in_(event_ids))

                        q = q.group_by(Inscription.nom_inscrit, Inscription.prenom_inscrit)
                        q = q.order_by(func.sum(Classer.points).desc())

                        rows = q.all()
                        for nom, prenom, pts in rows:
                                lesInscrits.append({'nom_inscrit': nom, 'prenom_inscrit': prenom, 'points': int(pts or 0)})

                years_q = db.session.query(extract('year', Evenement.date).label('year')).distinct().order_by(extract('year', Evenement.date).desc())
                saisons = [int(row.year) for row in years_q if row.year is not None]

                return render_template('event_classement.html', 
                                                           inscrits=lesInscrits,
                                                           disciplines=disciplines,
                                                           coops=coops,
                                                           sexes=sexes_display,
                                                           categorie=categorie,
                                                           saison=saison,
                                                           niveau=niveau,
                                                           saisons=saisons,
                                                           event_count=event_count)