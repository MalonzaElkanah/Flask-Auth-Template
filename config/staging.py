import os
from dotenv import load_dotenv
from datetime import timedelta


application_root = "/".join(os.path.dirname(__file__).split("/")[:-1])
dotenv_path = os.path.join(application_root, ".env")
load_dotenv(dotenv_path)


class StagingConfig(object):
    TESTING = True
    LOG_LEVEL = "INFO"
    SECRET_KEY = os.getenv("SECRET_KEY")
    EMAIL_TOKEN_SECRET_KEY = os.getenv("EMAIL_TOKEN_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("STAGE_DATABASE_USER")}:{os.getenv("STAGE_DATABASE_PASSWORD")}@{os.getenv("STAGE_DATABASE_HOST")}:{os.getenv("STAGE_DATABASE_PORT")}/{os.getenv("STAGE_DATABASE_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", True)
    # JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    UPLOAD_FOLDER = os.path.join(application_root, "instance/uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
