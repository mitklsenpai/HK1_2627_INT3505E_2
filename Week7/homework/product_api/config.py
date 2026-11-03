import os

class DefaultConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-not-for-prod")
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL", "sqlite:///../db/homework.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

class TestConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOG_LEVEL = "WARNING"
