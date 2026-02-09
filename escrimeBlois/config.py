import os



class Config:
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or ("sqlite:///" + os.path.join(basedir, "escrimeBlois.db"))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = "b'O?\x02\xdf'"

    # Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "Flask Mailer"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER =  os.environ.get("MAIL_DEFAULT_SENDER_EMAIL"),
    
