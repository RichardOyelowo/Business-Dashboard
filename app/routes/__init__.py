from .main import index_bp
from .orders import orders_bp
from .customers import customers_bp
from .imports import imports_bp


def register_routes(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(imports_bp)
