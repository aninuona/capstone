import os

class DevelopmentConfig:
    # a Secret key for session security, change this to something random before going live
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-before-deploying")

    # MySQL connection string: mysql+pymysql://user:password@host/database_name
    # Update the values below to match your local MySQL setup
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:yourpassword@localhost/syllabus_decoder"
    )

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
