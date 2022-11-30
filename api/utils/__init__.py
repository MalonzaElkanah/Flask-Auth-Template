import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


logging.basicConfig()
logging.root.setLevel(getattr(logging, os.getenv("LOG_LEVEL", "INFO")))

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name, name="Main"):
    """Creating application"""

    # create and configure the app
    logging.info(f"Flask App: Creating {name} application instance...")
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(config_name)

    # Logging Configurations without showing Database Password or secret key
    app_config = dict(app.config)
    app_config.update({
        'SECRET_KEY': '<not displayed for security reasons>',
        'SQLALCHEMY_DATABASE_URI': '<not displayed for security reasons>'
    })
    logging.info(f"Flask App: {name} application loaded the following configuration... {app_config}")

    # Register Database, Model and Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    return app
