from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False,  index=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"


def hash_password(password):
        return generate_password_hash(password)


def validate_password(user_password,password):
        return check_password_hash(user_password, password)

    