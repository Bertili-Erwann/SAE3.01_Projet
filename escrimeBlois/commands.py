import click
import logging
from hashlib import sha256
from .models import Personne
from .app import app, db
from sqlalchemy import func
lg = logging.getLogger(__name__)


# @app.cli.command()
# @click.argument('filename')
# def loaddb(filename):
#     """Creates the tables and populates them with data."""
#     # recréer la base
#     db.drop_all()
#     db.create_all()

#     import yaml
#     from .models import Auteur, Livre

#     with open(filename, 'r', encoding='utf-8') as file:
#         lesLivres = yaml.safe_load(file) or []

#     # helper to get a sensible PK attribute name from an author object
#     def _get_id(obj):
#         for attr in ('id', 'idA', 'id_auteur', 'idAuteur', 'auteur_id'):
#             if hasattr(obj, attr):
#                 return getattr(obj, attr)
#         return None

#     # première passe : création de tous les auteurs (évite doublons)
#     lesAuteurs = {}
#     for livre in lesLivres:
#         auteur_name = livre.get('author') or livre.get('auteur')
#         if not auteur_name:
#             continue
#         if auteur_name in lesAuteurs:
#             continue
#         auteur_obj = Auteur(nom=auteur_name) if hasattr(Auteur, 'nom') else Auteur(name=auteur_name)
#         db.session.add(auteur_obj)
#         # flush pour obtenir un id si nécessaire sans committer encore
#         db.session.flush()
#         lesAuteurs[auteur_name] = auteur_obj
#     db.session.commit()

#     # deuxième passe : création de tous les livres
#     for livre in lesLivres:
#         auteur_name = livre.get('author') or livre.get('auteur')
#         auteur_obj = lesAuteurs.get(auteur_name)
#         if not auteur_obj:
#             continue

#         # construire kwargs en essayant plusieurs noms de champs courants
#         kwargs = {}
#         if 'price' in livre:
#             if hasattr(Livre, 'prix'):
#                 kwargs['prix'] = livre.get('price')
#             elif hasattr(Livre, 'price'):
#                 kwargs['price'] = livre.get('price')
#         if 'title' in livre:
#             if hasattr(Livre, 'titre'):
#                 kwargs['titre'] = livre.get('title')
#             elif hasattr(Livre, 'title'):
#                 kwargs['title'] = livre.get('title')
#         if 'url' in livre:
#             if hasattr(Livre, 'url'):
#                 kwargs['url'] = livre.get('url')
#         if 'img' in livre:
#             if hasattr(Livre, 'img'):
#                 kwargs['img'] = livre.get('img')

#         # essayer d'attacher l'auteur soit par clé étrangère soit par relation
#         auteur_pk = _get_id(auteur_obj)
#         if auteur_pk is not None:
#             # trouver le nom probable du champ FK sur Livre
#             if hasattr(Livre, 'auteur_id'):
#                 kwargs['auteur_id'] = auteur_pk
#             elif hasattr(Livre, 'id_auteur'):
#                 kwargs['id_auteur'] = auteur_pk
#             elif hasattr(Livre, 'auteurId'):
#                 kwargs['auteurId'] = auteur_pk
#             else:
#                 # dernier recours : passer l'objet relationnel si le modèle l'accepte
#                 kwargs['auteur'] = auteur_obj
#         else:
#             kwargs['auteur'] = auteur_obj

#         livre_obj = Livre(**kwargs)
#         db.session.add(livre_obj)

#     db.session.commit()
#     lg.warning('Database initialized!')




@app.cli.command()
def syncdb():
    """Crée les tables de la BD"""
    db.create_all()
    lg.warning('Base de donnée synchronisée!')


def maxutilisateur() -> int:
    """donne l'id de l'utilisateur le plus grand de la BD, 0 si il n'y en à pas
    """
    max_id = db.session.query(func.max(Personne.id_personne)).scalar()
    return (int(max_id)+1) if max_id is not None else 1


@app.cli.command()
@click.argument('nom')
@click.argument('prenom')
@click.argument('role_user')
@click.argument('pwd')
@click.argument('mail')
def nouvpers(nom, prenom, role_user, pwd, mail):
    """Ajoute un nouveau membre dans la base de donnée 
    """
    
    if Personne.query.filter_by(email_personne=mail).first():
        lg.warning('User %s existe déjà', mail)
        return
    m = sha256()
    m.update(pwd.encode('utf-8'))
    
    pers = Personne(id_personne=maxutilisateur(),
                      mdp=m.hexdigest(),
                      role=role_user,
                      nom_personne=nom,
                      prenom_personne=prenom,
                      email_personne=mail)

    db.session.add(pers)
    db.session.commit()

    lg.info('Utilisateur %s crée',prenom)


