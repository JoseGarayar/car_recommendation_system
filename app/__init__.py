# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# Python
from datetime import timedelta
# App
from constants import (
    ENV,
    SECRET_KEY,
    JWT_SECRET_KEY,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
    app.config['ENV']='development'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ERROR_404_HELP'] = False
    app.config['DEBUG'] = True if ENV == 'development' else False
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from models import User
        db.create_all()

    # Register routes
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register CLI commands
    from commands import register_commands
    register_commands(app)

    return app