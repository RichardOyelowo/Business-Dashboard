from .decorators import login_required
from .routes import auth
from .utils import current_user


def register_auth(app):
    app.register_blueprint(auth)