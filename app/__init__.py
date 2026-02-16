import os
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, mail
from app.auth import register_auth
from app.routes import register_routes
from app.config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_auth(app)

    return app