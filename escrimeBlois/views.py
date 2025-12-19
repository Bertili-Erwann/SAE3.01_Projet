from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from hashlib import sha256
from datetime import date, datetime
from sqlalchemy import extract
from .app import app, db
from .models import *
from escrimeBlois.models import (
    Formulaire,
    Personne,
    Demande_inscription,
    Inscription,
    Evenement,
    Article,  # Ajouté pour les nouvelles routes articles
    Image,  # Ajouté pour la gestion des images dans ajouter_article
    Posseder,  # Ajouté pour le lien article ↔ image
)
from escrimeBlois.form import (
    FormInscription,
    FormInscriptionEvent,
    FormFormulaire,
    FormRechercheArticle,  # Ajouté pour la recherche sur l'index
    FormCommentaire,  # Ajouté pour les commentaires
)
import os


# ======================================== GESTION FOOTER (Accessible partout) ========================================
@app.route('/insert_formulaire', methods=['POST'])
def insert_formulaire():
    form = FormFormulaire()
    if form.validate_on_submit():
        form.commit_formulaire()
        flash("Votre message a été envoyé avec succès.", "success")
    else:
        flash("Erreur lors de l'envoi du formulaire.", "error")
    return redirect(request.referrer or url_for('index'))


# ======================================== PAGES GLOBAL (Accessible partout) ========================================


@app.route('/', )
@app.route('/index/')
def index():
    return render_template("index.html", formRech=FormRechercheArticle())


@app.route('/demande_article', methods=['GET'])
def demande_article():
    formRech = FormRechercheArticle()
    if request.method == 'GET':
        laRecherche = request.args["recherche"]
        date = request.args["choix_year"].split(
            "-")  # index 0 c'est le mois et 1 l'année

        listarticle = list(
            Article.query.filter(
                extract('month', Article.date_publication) == date[0]
                and extract('year', Article.date_publication)
                == date[1]).filter(Article.titre.contains(laRecherche)))

        return render_template('articles.html',
                               articles=listarticle,
                               recherche=laRecherche,date=date)
    else:
        return render_template("index.html", formRech=formRech())


@app.route("/historique/")
def historique():
    return render_template("historique.html", form=FormFormulaire())


@app.route("/renseignement/")
def renseignement():
    return render_template("renseignement.html",
                           title="renseignement",
                           form=FormFormulaire())


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Personne.query.filter_by(email_personne=email).first()

        if user:
            m = sha256()
            m.update(password.encode("utf-8"))
            hashed_password = m.hexdigest()

            if user.mdp == hashed_password or user.mdp == password:
                login_user(user)
                flash("Connexion réussie !", "success")
                if user.role == "membre":
                    return redirect(url_for("infos_persos"))
                elif user.role == "responsable":
                    return redirect(url_for("ajouter_article"))
                else:
                    return redirect(url_for("index"))
            else:
                flash("Mot de passe incorrect.", "error")
        else:
            flash("Email inconnu.", "error")
    return render_template("login.html", form=FormFormulaire())


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/inscription/", )
def inscription():
    form = FormInscription(request.form)
    return render_template("inscription.html",
                           formInscription=form,
                           form=FormFormulaire())


@app.route("/inscription/insert", methods=("POST", ))
def insert_inscription():
    form = FormInscription()
    if form.validate_on_submit():
        form.commit_inscription()

    return render_template("inscription.html",
                           formInscription=form,
                           form=FormFormulaire())


@app.route("/mdp_oublier_envoyer_code/")
def mdp_oublier_envoyer_code():
    return render_template("mdp_oublier_envoyer_code.html",
                           form=FormFormulaire())


@app.route("/mdp_oublier_code/")
def mdp_oublier_code():
    return render_template("mdp_oublier_code.html", form=FormFormulaire())


@app.route("/mdp_oublier_confirmer_mdp/", methods=["GET", "POST"])
def mdp_oublier_confirmer_mdp():
    if request.method == "POST":
        newpassword = request.form.get("newpassword")
        newpasswordconfirm = request.form.get("newpasswordconfirm")

        if newpassword != newpasswordconfirm:
            return render_template("mdp_oublier_confirmer_mdp.html",
                                   form=FormFormulaire())

        # Ici, tu peux ajouter la logique pour mettre à jour le mot de passe en base
        return redirect(url_for("login"))

    return render_template("mdp_oublier_confirmer_mdp.html",
                           form=FormFormulaire())


@app.route('/article/<ida>/view')
def view_article(ida):
    art = Article.query.get(ida)
    form = FormCommentaire()
    return render_template('article_view.html', article=art, formCom=form)


@app.route('/article/<ida>/comment', methods=["POST"])
def insert_commentaire(ida):
    art = Article.query.get(ida)
    form = FormCommentaire()
    if form.is_submitted():
        form.envoyer_commentaire(ida)
        return redirect(url_for('view_article', ida=ida))
    return render_template('article_view.html', article=art, formCom=form)


@app.route('/evenement/résultats')
def resultat():
    competitions = Evenement.query.filter_by(
        type_evenement='competition').all()

    selected_competition_id = request.args.get('competition')
    classements = []

    if selected_competition_id:
        classements = db.session.query(Classer, Inscription, Personne).join(
            Inscription,
            Classer.id_competition == Inscription.id_inscription).outerjoin(
                Personne, Inscription.email == Personne.email_personne).filter(
                    Classer.id_inscription ==
                    selected_competition_id).order_by(
                        Classer.point.desc()).all()

    return render_template("resultat.html",
                           competitions=competitions,
                           classements=classements,
                           selected_id=selected_competition_id,
                           form=FormFormulaire())


@app.route('/evenement/calendrier')
def calendrier():
    types_selectionnes = request.args.getlist('type')
    ville_recherche = request.args.get('ville')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    categorie = request.args.get('categorie')
    niveau = request.args.get('niveau')
    query = Evenement.query

    if types_selectionnes:
        query = query.filter(Evenement.type_evenement.in_(types_selectionnes))
    if ville_recherche:
        query = query.filter(Evenement.lieu.ilike(f'%{ville_recherche}%'))
    if date_debut:
        query = query.filter(Evenement.date >= date_debut)
    if date_fin:
        query = query.filter(Evenement.date <= date_fin)
    if categorie and categorie != "Toutes catégories":
        query = query.filter(Evenement.categorie == categorie)
    if niveau and niveau != "Niveaux":
        query = query.filter(Evenement.niveau == niveau)

    query = query.order_by(Evenement.date.asc())
    evenements = query.all()

    return render_template('calendrier_event.html',
                           evenements=evenements,
                           filtres=request.args,
                           types_selectionnes=types_selectionnes,
                           form=FormFormulaire())


@app.route('/evenement/calendrier/consulter/<int:id_evenement>')
def consulter_evenement(id_evenement):
    evenement = Evenement.query.get_or_404(id_evenement)
    return render_template('consulter_evenement.html',
                           evenement=evenement,
                           form=FormFormulaire())


@app.route('/evenement/inscription/<int:id_evenement>',
           methods=['GET', 'POST'])
def inscription_event(id_evenement):
    evenement = Evenement.query.get_or_404(id_evenement)

    if evenement.type_evenement == 'reunion':
        flash("L'inscription n'est pas disponible pour les réunions.", 'error')
        return redirect(
            url_for('consulter_evenement', id_evenement=id_evenement))

    if current_user.is_authenticated:
        deja_inscrit = Inscription.query.filter_by(
            id_evenement=id_evenement,
            nom=current_user.nom_personne,
            prenom=current_user.prenom_personne).first()
        if deja_inscrit:
            flash('Vous êtes déjà inscrit à cet événement.', 'info')
        else:
            inscription = Inscription(
                id_evenement=id_evenement,
                nom=current_user.nom_personne,
                prenom=current_user.prenom_personne,
                email=current_user.email_personne,
                date_naissance=current_user.date_naissance,
                sexe=current_user.sexe)
            db.session.add(inscription)
            db.session.commit()
        return redirect(
            url_for('consulter_evenement',
                    id_evenement=id_evenement,
                    inscription_success=True))

    form = FormInscriptionEvent()
    if request.method == 'GET' and evenement.categorie:
        form.categorie.data = evenement.categorie

    if form.validate_on_submit():
        filename = None
        if form.justificatif.data:
            f = form.justificatif.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        inscription = Inscription(id_evenement=id_evenement,
                                  nom=form.nom.data,
                                  prenom=form.prenom.data,
                                  email=form.email.data,
                                  date_naissance=form.date_naissance.data,
                                  sexe=form.sexe.data,
                                  categorie=form.categorie.data,
                                  justificatif=filename)
        db.session.add(inscription)
        db.session.commit()
        return redirect(
            url_for('consulter_evenement',
                    id_evenement=id_evenement,
                    inscription_success=True))

    return render_template('inscription_event.html',
                           formInsc=form,
                           id_evenement=id_evenement,
                           evenement=evenement,
                           form=FormFormulaire())


# ======================================== PAGES ADMIN ========================================


@app.route("/admin/")
@app.route("/admin/gestion_inscription/club")
def admin_inscription_club():
    demandes = Demande_inscription.query.all()
    return render_template("admin_gestion_inscription_club.html",
                           demandes=demandes,
                           form=FormFormulaire())


@app.route("/admin/gestion_inscription/club/view/<int:id_inscription>",
           methods=["GET", "POST"])
def admin_inscription_club_view(id_inscription):
    demande = Demande_inscription.query.get_or_404(id_inscription)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "accepter":
            nouveau_membre = Personne(
                mdp=demande.mot_de_passe,
                nom_personne=demande.nom,
                prenom_personne=demande.prenom,
                email_personne=demande.adresse_mail,
                telephone=demande.num_tel,
                sexe=demande.sexe,
                adresse=demande.adresse_postale,
                date_naissance=demande.date_naissance,
                eleve=demande.eleve,
                arme_principale="Non défini",
                niveau="Débutant",
                role="membre",
            )
            db.session.add(nouveau_membre)
            db.session.delete(demande)
            db.session.commit()
        elif action == "refuser":
            db.session.delete(demande)
            db.session.commit()
        return redirect(url_for("admin_inscription_club"))
    return render_template("admin_gestion_inscription_club_view.html",
                           demande=demande,
                           form=FormFormulaire())


@app.route("/admin/gestion_inscription/evenement")
def admin_inscription_evenement():
    inscriptions = Inscription.query.all()
    return render_template("admin_gestion_inscription_evenement.html",
                           inscriptions=inscriptions,
                           form=FormFormulaire())


@app.route("/admin/gestion_inscription/evenement/view/<int:id_inscription>",
           methods=["GET", "POST"])
def admin_inscription_evenement_view(id_inscription):
    inscription = Inscription.query.get_or_404(id_inscription)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "refuser":
            db.session.delete(inscription)
            db.session.commit()
        return redirect(url_for("admin_inscription_evenement"))
    return render_template("admin_gestion_inscription_evenement_view.html",
                           inscription=inscription,
                           form=FormFormulaire())


@app.route("/admin/miseajour/membres")
def admin_miseajour_membres():
    les_responsables = []
    les_membres = []
    personne = Personne.query.all()
    for e in personne:
        if e.role == "responsable":
            les_responsables.append(e)
        elif e.role == "membre":
            les_membres.append(e)
    return render_template("admin_miseajour_membres.html",
                           membres=les_membres,
                           responsables=les_responsables,
                           form=FormFormulaire())


@app.route("/admin/supprimer/membre/<int:id_personne>", methods=["POST"])
def supprimer_membre(id_personne):
    try:
        personne = Personne.query.get(id_personne)
        if personne:
            db.session.delete(personne)
            db.session.commit()
            flash("Membre supprimé avec succès", "success")
        else:
            flash("Membre non trouvé", "error")
    except Exception as e:
        db.session.rollback()
        flash("Erreur lors de la suppression", "error")
    return redirect(url_for("admin_miseajour_membres"))


@app.route('/admin/creation_competition', methods=['GET', 'POST'])
def admin_comp():
    if request.method == 'POST':
        name = request.form.get('name_create_event')
        categories = request.form.get('categories_create_event')
        date_str = request.form.get('date_create_event')
        hour_str = request.form.get('hour_create_event')
        location = request.form.get('location_create_event')
        description = request.form.get('bottom_create_event')
        discipline = request.form.get('discipline_comp')
        sexe = request.form.get('sexe_comp')
        jeu = request.form.get('jeu_comp')
        niveau = request.form.get('niveau_comp')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        hour = datetime.strptime(hour_str, '%H:%M').time()
        heure_minutes = hour.hour * 60 + hour.minute

        nouvel_evenement = Evenement(nom=name,
                                     date=date,
                                     heure=heure_minutes,
                                     categorie=categories,
                                     lieu=location,
                                     description=description,
                                     sexe=sexe,
                                     niveau=niveau,
                                     discipline=discipline,
                                     cooperative=jeu,
                                     type_evenement="competition")

        db.session.add(nouvel_evenement)
        db.session.commit()
        flash('Compétition créée avec succès !', 'success')
        return redirect(url_for('admin_comp'))

    return render_template('admin_crea_comp.html', form=FormFormulaire())


# ======================================== PAGES RESPONSABLE ========================================


@app.route("/responsable/")
@app.route("/responsable/gestion_formulaire/")
def gest_form():
    lesFormulaires = Formulaire.query.all()
    return render_template("gestion_formulaire.html",
                           formulaires=lesFormulaires,
                           form=FormFormulaire())


@app.route("/responsable/consultation_formulaire/<id_formulaire>/")
def consult_form(id_formulaire):
    unForm = Formulaire.query.get(id_formulaire)
    return render_template("consultation_form.html",
                           selectedFormulaire=unForm,
                           form=FormFormulaire())


@app.route("/responsable/ajouter_article/", methods=["GET", "POST"])
def ajouter_article():
    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description")
        theme = request.form.get("theme")
        commentable = True if request.form.get(
            "commentable") == "on" else False
        responsable_id = 1  # À remplacer par current_user.id_personne si besoin
        fichiers = request.files.getlist("fichiers")

        article = Article(
            titre=titre,
            description=description,
            categorie=theme,
            commentable=commentable,
            responsable_id=responsable_id,
            date_publication=date.today(),
        )
        db.session.add(article)
        db.session.commit()

        first_image = True
        for fichier in fichiers:
            if fichier and fichier.filename != "":
                chemin_fichier = os.path.join(app.config["UPLOAD_FOLDER"],
                                              fichier.filename)
                fichier.save(chemin_fichier)

                image = Image(nom_image=fichier.filename[:15],
                              url_image=fichier.filename[:60])
                db.session.add(image)
                db.session.commit()

                posseder = Posseder(id_image=image.id_image,
                                    id_article=article.id_article,
                                    miniature=first_image)
                db.session.add(posseder)
                db.session.commit()
                first_image = False

        flash("Article ajouté avec succès ✅", "success")
        return redirect(url_for("ajouter_article"))

    return render_template("ajout_article.html", form=FormFormulaire())


@app.route("/responsable/creer_evenement/", methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name_create_event')
        categories = request.form.get('categories_create_event')
        date_str = request.form.get('date_create_event')
        hour_str = request.form.get('hour_create_event')
        location = request.form.get('location_create_event')
        description = request.form.get('bottom_create_event')
        type = request.form.get('types_create_event')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        hour = datetime.strptime(hour_str, '%H:%M').time()
        heure_minutes = hour.hour * 60 + hour.minute

        nouvel_evenement = Evenement(nom=name,
                                     date=date,
                                     heure=heure_minutes,
                                     categorie=categories,
                                     lieu=location,
                                     description=description,
                                     sexe=None,
                                     niveau=None,
                                     discipline=None,
                                     cooperative=None,
                                     type_evenement=type)

        db.session.add(nouvel_evenement)
        db.session.commit()
        flash('Événement créé avec succès !', 'success')
        return redirect(url_for('create_event'))

    return render_template('resp_creation_event.html', form=FormFormulaire())


# Configuration du dossier d'upload (placée ici comme dans develop)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ======================================== PAGES MEMBRES ========================================


@app.route("/membre/")
@app.route("/membre/information_personnel/")
@login_required
def infos_persos():
    if current_user.role != "membre":
        return redirect(url_for("index"))
    return render_template("infos_persos_espMembre.html",
                           personne=current_user,
                           form=FormFormulaire())


# Nouvelle route : événements auxquels le membre est inscrit
@app.route('/membre/event_inscrits/')
@login_required
def event_inscrits():
    if current_user.role != 'membre':
        return redirect(url_for('index'))

    inscriptions = Inscription.query.filter_by(
        nom=current_user.nom_personne,
        prenom=current_user.prenom_personne).all()

    evenements_inscrits = [
        insc.evenement for insc in inscriptions if insc.evenement
    ]

    return render_template('event_inscrits.html',
                           evenements=evenements_inscrits,
                           form=FormFormulaire())


# Nouvelle route : consultation détaillée d'un événement depuis l'espace membre
@app.route('/consult_event/<int:id_event>/')
@login_required
def consult_event(id_event):
    if current_user.role != 'membre':
        return redirect(url_for('index'))

    event = Evenement.query.get_or_404(id_event)
    return render_template('consult_event.html',
                           event=event,
                           form=FormFormulaire())


@app.route("/membre/information_personnel/changer_mdp/", methods=["POST"])
@login_required
def change_password():
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not new_password or not confirm_password:
        flash("Les deux champs de mot de passe sont requis.", "error")
        return redirect(url_for("infos_persos"))

    if new_password != confirm_password:
        flash("Les mots de passe ne correspondent pas.", "error")
        return redirect(url_for("infos_persos"))

    if len(new_password) < 8:
        flash("Le mot de passe doit contenir au moins 8 caractères.", "error")
        return redirect(url_for("infos_persos"))

    if not any(c.isalpha()
               for c in new_password) or not any(c.isdigit()
                                                 for c in new_password):
        flash(
            "Le mot de passe doit contenir au moins une lettre et un chiffre.",
            "error")
        return redirect(url_for("infos_persos"))

    try:
        m = sha256()
        m.update(new_password.encode("utf-8"))
        hashed_password = m.hexdigest()
        current_user.mdp = hashed_password
        db.session.commit()
        flash("Votre mot de passe a été mis à jour avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(
            "Une erreur est survenue lors de la mise à jour du mot de passe.",
            "error")
        app.logger.error(
            f"Erreur lors du changement de mot de passe: {str(e)}")

    return redirect(url_for("infos_persos"))


@app.route("/membre/information_personnel/updt_arme_principale",
           methods=["POST"])
@login_required
def update_arme():
    arme = request.form.get("arme_principale")
    try:
        current_user.arme_principale = arme
        db.session.commit()
        flash("Votre arme principale a été mise à jour avec succès.",
              "success")
    except Exception as e:
        db.session.rollback()
        flash("Une erreur est survenue lors de la mise à jour de l'arme.",
              "error")
        app.logger.error(f"Erreur lors de la mise à jour de l'arme: {str(e)}")
    return redirect(url_for('infos_persos'))
