from app.extensions import db
from flask import g, session
from app.models import User
from app import create_app


app = create_app()

@app.before_request
def activate_current_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None

@app.context_processor
def inject_user():
    return dict(current_user=g.user)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()