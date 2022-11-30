import os


TESTING = False
LOG_LEVEL = "DEBUG"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DEV_DATABASE_USER")}:{os.getenv("DEV_DATABASE_PASSWORD")}@{os.getenv("DEV_DATABASE_HOST")}:{os.getenv("DEV_DATABASE_PORT")}/{os.getenv("DEV_DATABASE_NAME")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
