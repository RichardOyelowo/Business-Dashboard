import os
from flask import Flask, g, session
from app.extensions import db, migrate, mail
from app.auth import register_auth
from app.routes import register_routes
from app.config import DevelopmentConfig, ProductionConfig
from app.models import User


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

    @app.before_request
    def activate_current_user():
        user_id = session.get("user_id")
        g.user = db.session.get(User, user_id) if user_id else None

    @app.context_processor
    def inject_user():
        return {"current_user": getattr(g, "user", None)}

    return app
