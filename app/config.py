import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("BUSINESS_DASHBOARD_EMAIL")
    MAIL_PASSWORD = os.environ.get("BUSINESS_DASHBOARD_EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Business Dashboard", MAIL_USERNAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///dev.db")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


for name in ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_DEFAULT_SENDER", "MAIL_SERVER"]:
    if getattr(Config, name) is None:
        print(f"Missing: {name}")


