import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///interview.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # For production, you can uncomment and set your PostgreSQL URL like this:
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     "DATABASE_URL", "postgresql://username:password@host:5432/dbname"
    # )
    # Ensure SECRET_KEY is set as an environment variable in production
