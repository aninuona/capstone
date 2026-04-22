import os

class DevelopmentConfig:
    # Secret key for session security, CHANGE BEFORE FINAL
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-before-deploying")

    SQLALCHEMY_DATABASE_URI = "sqlite:///syllabus.db"

    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True


class ProductionConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


# Dictionary so app.py can look up the right config by environment name
config = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}
