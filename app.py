import os

from flask import Flask

from api.urls import api_urls


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object('config')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Urls
    api_urls(app)

    print(app.config)

    return app
    