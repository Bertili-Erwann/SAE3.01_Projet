from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import validates
from sqlalchemy_media import File
from sqlalchemy import JSON


@login_manager.user_loader
def load_user(id: int) -> "Personne":
    """
    Charge un utilisateur par son ID pour Flask-Login.
    
    Args:
        id (int): L'ID de la personne.
    
    Returns:
        Personne: L'objet Personne correspondant, ou None si introuvable.
    """
    return Personne.query.get(id)


class Personne(UserMixin, db.Model):
    """
    Modèle représentant une personne (utilisateur) dans le système.
    
    Attributs:
        id_personne (int): Clé primaire.
        mdp (str): Mot de passe.
        nom_personne (str): Nom de famille.
        prenom_personne (str): Prénom.
        email_personne (str): Adresse email.
        telephone (str): Numéro de telephone
        sexe (str): Sexe (1 caractère).
        adresse (str): Adresse postale.
        date_naissance (Date): Date de naissance.
        eleve (bool): Indique si la personne est étudiante.
        arme_principale (str): Arme principale (épée, fleuret, sabre).
        niveau (str): Niveau de compétence.
        role (str): Rôle ('personne', 'membre', 'responsable', 'admin').
        telephone (str): Numéro de téléphone.
    """
    id_personne = db.Column(db.Integer, primary_key=True)
    mdp = db.Column(db.String(64))
    nom_personne = db.Column(db.String(64))
    prenom_personne = db.Column(db.String(64))
    email_personne = db.Column(db.String(64))
    telephone = db.Column(db.String(64))
    sexe = db.Column(db.String(1))
    adresse = db.Column(db.String(64))
    date_naissance = db.Column(db.Date)
    eleve = db.Column(db.Boolean)
    arme_principale = db.Column(db.String(30))
    niveau = db.Column(db.String(20))
    role = db.Column(db.String(10))

    @validates('role')
    def validate_role(self, key: str, value: str) -> str:
        """
        Valide le rôle de la personne selon les règles métier.
        
        Args:
            key (str): Le nom de l'attribut ('role').
            value (str): La valeur du rôle.
        
        Returns:
            str: La valeur validée.
        
        Raises:
            ValueError: Si les champs requis ne sont pas remplis ou si des champs en trop sont présents.
        """
        match value:
            case "membre" | "responsable":
            # TOUS les champs requis doivent être remplis
                if (self.eleve is None or self.arme_principale is None or self.niveau is None or 
                    self.sexe is None or self.adresse is None or self.date_naissance is None):
                    raise ValueError(f"Le  '{value}' n'a pas rempli un des champs requis")
            case "personne" | "admin":
                if self.eleve is not None or self.arme_principale is not None or self.niveau is not None:
                    raise ValueError(f"'{value}' a des informations en trop")
        return value

    def get_id(self):
        return self.id_personne

    def __repr__(self) -> str:
        """
        Représentation simple de la personne.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Personne {self.id_personne}"

    def __str__(self) -> str:
        """
        Représentation simple du nom de la personne.
        
        Returns:
            str: Le nom complet de la personne.
        """
        return f"{self.nom_personne} {self.prenom_personne}"


class Demande_inscription(db.Model):
    """
    Modèle représentant une demande d'inscription.
    
    Attributs:
        id_inscription (int): Clé primaire.
        nom (str): Nom de famille.
        prenom (str): Prénom.
        mot_de_passe (str): Mot de passe.
        sexe (str): Sexe (1 caractère).
        date_naissance (Date): Date de naissance.
        num_tel (str): Numéro de téléphone.
        adresse_mail (str): Adresse email.
        adresse_postale (str): Adresse postale.
        scolarisee (bool): Indique si la personne est scolarisée.
        eleve (bool): Indique si la personne est étudiante.
        justificatif (str): Justificatif fourni.
    """
    id_inscription = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64))
    prenom = db.Column(db.String(64))
    mot_de_passe = db.Column(db.String(64))
    sexe = db.Column(db.String(1))
    date_naissance = db.Column(db.Date)
    num_tel = db.Column(db.String(10))
    adresse_mail = db.Column(db.String(64))
    adresse_postale = db.Column(db.String(64))
    eleve = db.Column(db.Boolean)
    justificatif = db.Column(File.as_mutable(JSON))

    def __repr__(self) -> str:
        """
        Représentation simple de la demande d'inscription.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Demande_inscription {self.id_inscription}"

    def __str__(self) -> str:
        """
        Représentation simple du nom de la personne.
        
        Returns:
            str: Le nom complet de la personne.
        """
        return f"{self.nom} {self.prenom}"


class Evenement(db.Model):
    """
    Modèle représentant un événement (compétition ou autre).
    
    Attributs:
        id_evenement (int): Clé primaire.
        date (Date): Date de l'événement.
        heure (int): Heure de l'événement.
        categorie (str): Catégorie de l'événement.
        lieu (str): Lieu de l'événement.
        description (str): Description de l'événement.
        niveau (str): Niveau requis (pour compétitions).
        discipline (str): Discipline (pour compétitions).
        cooperative (str): Partenaire coopératif (pour compétitions).
        type_evenement (str): Type ('competition' ou autre).
    """
    id_evenement = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64))
    date = db.Column(db.Date)
    heure = db.Column(db.Integer)
    categorie = db.Column(db.String(30))
    lieu = db.Column(db.String(64))
    description = db.Column(db.String(255))

    niveau = db.Column(db.String(10))
    discipline = db.Column(db.String(60))
    cooperative = db.Column(db.String(60))

    type_evenement = db.Column(db.String(64))

    @validates('type_evenement')
    def validate_attributs_evenement(self, key: str, value: str) -> str:
        """
        Valide les attributs selon le type d'événement.
        
        Args:
            key (str): Le nom de l'attribut ('type_evenement').
            value (str): La valeur du type.
        
        Returns:
            str: La valeur validée.
        
        Raises:
            ValueError: Si les champs requis ne sont pas remplis ou si des champs en trop sont présents.
        """
        match value:
            case "competition":
                if self.niveau is None or self.discipline is None or self.cooperative is None:
                    raise ValueError(
                        f"'{value}' n'a pas rempli un des champs requis")
            case _:
                if self.niveau is not None or self.discipline is not None or self.cooperative is not None:
                    raise ValueError(f"'{value}' a des informations en trop")
        return value

    def __repr__(self) -> str:
        """
        Représentation simple de l'événement.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Evenement {self.id_evenement}"

    def __str__(self) -> str:
        """
        Représentation simple du type d'événement.
        
        Returns:
            str: Le type de l'événement.
        """
        return self.type_evenement


class Inscription(db.Model):
    """
    Modèle représentant une inscription à un événement.
    
    Attributs:
        id_inscription (int): Clé primaire.
        id_evenement (int): Clé étrangère vers Evenement.
        nom (str): Nom de la personne.
        prenom (str): Prénom de la personne.
    """
    id_inscription = db.Column(db.Integer, primary_key=True)
    id_evenement = db.Column(db.Integer,
                             db.ForeignKey("evenement.id_evenement"))
    nom = db.Column(db.String(64))
    prenom = db.Column(db.String(64))
    email = db.Column(db.String(64))
    date_naissance = db.Column(db.Date)
    sexe = db.Column(db.String(1))
    justificatif = db.Column(db.String(255))
    
    # Relations
    evenement = db.relationship("Evenement", backref=db.backref("inscriptions", lazy="dynamic"))

    def __repr__(self) -> str:
        """
        Représentation simple de l'inscription.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Inscription {self.id_inscription}"

    def __str__(self) -> str:
        """
        Représentation simple de l'inscription.
        
        Returns:
            str: Le type de l'événement.
        """
        return f"Inscription {self.id_inscription}"


class Classer(db.Model):
    """
    Modèle représentant le classement dans une compétition.
    
    Attributs:
        id_competition (int): Clé étrangère vers Inscription, partie de la clé primaire.
        id_inscription (int): Clé étrangère vers Evenement, partie de la clé primaire.
        point (int): Points obtenus.
    """
    id_competition = db.Column(db.Integer,
                               db.ForeignKey("inscription.id_inscription"),
                               primary_key=True)
    id_inscription = db.Column(db.Integer,
                               db.ForeignKey("evenement.id_evenement"),
                               primary_key=True)
    point = db.Column(db.Integer)

    @validates('id_inscription')
    def validate_evenement_type(self, key: str, value: int) -> int:
        """
        Valide que l'événement est une compétition.
        
        Args:
            key (str): Le nom de l'attribut ('id_inscription').
            value (int): L'ID de l'événement.
        
        Returns:
            int: La valeur validée.
        
        Raises:
            ValueError: Si l'événement n'existe pas ou n'est pas une compétition.
        """
        ev = Evenement.query.get(value)
        if ev is None:
            raise ValueError(f"Événement {value} introuvable")
        if ev.type_evenement != 'competition':
            raise ValueError(
                f"L'événement {value} doit être de type competition ")
        return value

    def __repr__(self) -> str:
        """
        Représentation simple du classement.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Classer {self.id_competition}-{self.id_inscription}"

    def __str__(self) -> str:
        """
        Représentation simple des points.
        
        Returns:
            str: Les points obtenus.
        """
        return f"Points: {self.point}"


class Formulaire(db.Model):
    """
    Modèle représentant un formulaire de contact.
    
    Attributs:
        id_formulaire (int): Clé primaire.
        nom_auteur (str): Nom de l'auteur.
        prenom_auteur (str): Prénom de l'auteur.
        email_auteur (str): Email de l'auteur.
        objet (str): Objet du message.
        message (str): Contenu du message.
    """
    id_formulaire = db.Column(db.Integer, primary_key=True)
    nom_auteur = db.Column(db.String(64))
    prenom_auteur = db.Column(db.String(64))
    email_auteur = db.Column(db.String(64))
    objet = db.Column(db.String(100))
    message = db.Column(db.String(500))

    def __repr__(self) -> str:
        """
        Représentation simple du formulaire.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Formulaire {self.id_formulaire}"

    def __str__(self) -> str:
        """
        Représentation simple de l'objet du message.
        
        Returns:
            str: L'objet du message.
        """
        return self.objet


class Repondre(db.Model):
    """
    Modèle représentant une réponse à un formulaire par un responsable.
    
    Attributs:
        id_responsable (int): Clé étrangère vers Personne, partie de la clé primaire.
        id_formulaire (int): Clé étrangère vers Formulaire, partie de la clé primaire.
    """
    id_responsable = db.Column(db.Integer,
                               db.ForeignKey("personne.id_personne"),
                               primary_key=True)
    id_formulaire = db.Column(db.Integer,
                              db.ForeignKey("formulaire.id_formulaire"),
                              primary_key=True)

    @validates('id_responsable')
    def validate_responsable_type(self, key: str, value: int) -> int:
        """
        Valide que la personne est un responsable.
        
        Args:
            key (str): Le nom de l'attribut ('id_responsable').
            value (int): L'ID de la personne.
        
        Returns:
            int: La valeur validée.
        
        Raises:
            ValueError: Si la personne n'existe pas ou n'est pas un responsable.
        """
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        if pers.role != 'responsable':
            raise ValueError(
                f"La personne {value} doit être de type 'responsable' vous avez le type {pers.role}"
            )
        return value

    def __repr__(self) -> str:
        """
        Représentation simple de la réponse.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Repondre {self.id_responsable}-{self.id_formulaire}"

    def __str__(self) -> str:
        """
        Représentation simple de la réponse.
        
        Returns:
            str: Les identifiants de la responsable et du formulaire.
        """
        return f"Repondre {self.id_responsable}-{self.id_formulaire}"


class Article(db.Model):
    """
    Modèle représentant un article de blog ou d'actualité.
    
    Attributs:
        id_article (int): Clé primaire.
        titre (str): Titre de l'article.
        date_publication (Date): Date de publication.
        description (str): Contenu de l'article.
        categorie (str): Catégorie de l'article.
        commentable (bool): Indique si l'article est commentable.
        responsable_id (int): Clé étrangère vers Personne (responsable).
        responsable: Relation vers Personne.
    """
    id_article = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(64))
    date_publication = db.Column(db.Date)
    description = db.Column(db.String(1000))
    categorie = db.Column(db.String(20))
    commentable = db.Column(db.Boolean)
    responsable_id = db.ForeignKey("personne.id_personne")
    responsable = None

    @validates('id_responsable')
    def validate_responsable_type(self, key: str, value: int) -> int:
        """
        Valide que la personne est un responsable et établit la relation.
        
        Args:
            key (str): Le nom de l'attribut ('id_responsable').
            value (int): L'ID de la personne.
        
        Returns:
            int: La valeur validée.
        
        Raises:
            ValueError: Si la personne n'existe pas ou n'est pas un responsable.
        """
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        if pers.role != 'responsable':
            raise ValueError(
                f"La personne {value} doit être de type 'responsable' vous avez le type {pers.role}"
            )
        self.responsable = db.relationship("Personne",
                                           backref=db.backref("articles",
                                                              lazy="dynamic"))
        return value

    def __repr__(self) -> str:
        """
        Représentation simple de l'article.
        
        Returns:
            str: Chaîne basique avec l'ID.
        """
        return f"Article {self.id_article}"

    def __str__(self) -> str:
        """
        Représentation simple du titre de l'article.
        
        Returns:
            str: Le titre de l'article.
        """
        return self.titre


class Image(db.Model):
    """
    Modèle représentant une image de la base de donnée.
    
    Attributs:
        id_image (int): Clé primaire.
        nom_image (str): nom de l'image.
        url_image (str): url de l'image.
    """
    id_image = db.Column(db.Integer, primary_key=True)
    nom_image = db.Column(db.String(15))
    url_image = db.Column(db.String(60))


class Posseder(db.Model):
    """
    Modèle représentant l'association entre les articles et les images.
    
    Attributs:
        id_image (int): partie de la clé primaire, une clé étrangère référencant l'id de la table image.
        id_competition (int): partie de la clé primaire,une clé étrangère référencant l'id de la table article.
        miniature(bool): True si c'est la maniature d'un article, False sinon. 
    """
    id_image = db.Column(db.Integer,
                         db.ForeignKey("image.id_image"),
                         primary_key=True)
    id_article = db.Column(db.Integer,
                           db.ForeignKey("article.id_article"),
                           primary_key=True)
    miniature = db.Column(db.Boolean)


class Gerer(db.Model):
    """
    Modèle représentant la gestion des demandes d'inscription par un admin.
    
    Attributs:
        id_admin (int): Clé étrangère vers Personne (admin), partie de la clé primaire.
        id_inscription (int): Clé étrangère vers Demande_inscription, partie de la clé primaire.
    """
    id_admin = db.Column(db.Integer,
                         db.ForeignKey("personne.id_personne"),
                         primary_key=True)
    id_inscription = db.Column(
        db.Integer,
        db.ForeignKey("demande_inscription.id_inscription"),
        primary_key=True)

    @validates('id_admin')
    def validate_admin_type(self, key: str, value: int) -> int:
        """
        Valide que la personne est un admin.
        
        Args:
            key (str): Le nom de l'attribut ('id_admin').
            value (int): L'ID de la personne.
        
        Returns:
            int: La valeur validée.
        
        Raises:
            ValueError: Si la personne n'existe pas ou n'est pas un admin.
        """
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        if pers.role != 'admin':
            raise ValueError(
                f"La personne {value} doit être de type 'admin' vous avez le type {pers.role}"
            )
        return value
