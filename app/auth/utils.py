from app.models import User
from flask import g, session


def current_user():
    return g.get("user", None)
