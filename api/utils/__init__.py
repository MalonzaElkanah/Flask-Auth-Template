import logging
import os

from flask import Flask

logging.basicConfig()
logging.root.setLevel(getattr(logging, os.getenv("LOG_LEVEL", "INFO")))


def create_app(config_name, name="Main"):
    """Creating application"""

    # create and configure the app
    logging.info(f"Flask App: Creating {name} application instance...")
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object(config_name)
    logging.info(f"Flask App: {name} application loaded the following configuration... {app.config}")

    return app
