import os


def _env_bool(name: str, default: bool = False) -> bool:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}


class Config:
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or ("sqlite:///" + os.path.join(basedir, "escrimeBlois.db"))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or os.environ.get("FLASK_SECRET_KEY")
        or "dev-secret-key-change-me"
    )

    # Mail configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", True)
    MAIL_USE_SSL = _env_bool("MAIL_USE_SSL", False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    _sender_name = os.environ.get("MAIL_DEFAULT_SENDER_NAME", "Flask Mailer")
    _sender_email = os.environ.get("MAIL_DEFAULT_SENDER_EMAIL", "noreply@escrimeblois.com")
    MAIL_DEFAULT_SENDER = (_sender_name, _sender_email)

