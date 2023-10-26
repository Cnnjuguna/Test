import os
import secrets


from flask import Flask
from dotenv import load_dotenv
from .utilities import write_secret_key_to_env

from .extensions import db, migrate
from .extensions import login_manager, bcrypt
from .tasks import app as celery_app


from tasks import update_next_donation_dates

load_dotenv()

from .extensions import db, migrate, ma, login_manager, bcrypt


# Function to generate or retrieve the secret key
def generate_secret_key():
    secret_key = os.getenv("SECRET_KEY")
    if secret_key is None:
        secret_key = secrets.token_hex(32)
        os.environ["SECRET_KEY"] = secret_key  # Set the environment variable
        write_secret_key_to_env(secret_key)  # Writes  to .env
    return secret_key


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .routes.admin_bp import admin_bp
    from .routes.beneficiaries_bp import beneficiaries_bp
    from .routes.charities_bp import charities_bp
    from .routes.charity_applications_bp import charity_applications_bp
    from .routes.donations_bp import donations_bp
    from .routes.donors_bp import donors_bp
    from .routes.stories_bp import stories_bp
    from .routes.users_bp import users_bp

    # List of blueprints

    blueprints = [
        admin_bp,
        beneficiaries_bp,
        charities_bp,
        charity_applications_bp,
        donations_bp,
        donors_bp,
        stories_bp,
        users_bp,
    ]

    # Register the blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
