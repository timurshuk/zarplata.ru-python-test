from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db)

    from app import models

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
