from flask import Flask

from .extensions import db, migrate
from .extensions import login_manager, bcrypt

login_manager.init_app(app)
bcrypt.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.donordb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import user_bp, donation_bp, admin_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(donation_bp)
    app.register_blueprint(admin_bp)
