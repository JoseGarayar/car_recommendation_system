import os


ENV = os.environ.get('FLASK_ENV', 'development')
SECRET_KEY = os.environ.get("SECRET_KEY", None)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", None)
POSTGRES_DB = os.environ.get("POSTGRES_DB", None)