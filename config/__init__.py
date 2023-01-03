import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

current_env = os.getenv("ENVIRONMENT", "production").lower()


if current_env == "production":
    from config.production import ProductionConfig

    config_obj = ProductionConfig
elif current_env == "staging":
    from config.staging import StagingConfig

    config_obj = StagingConfig
elif current_env == "testing":
    from config.testing import TestingConfig

    config_obj = TestingConfig
elif current_env == "development":
    from config.development import DevelopmentConfig

    config_obj = DevelopmentConfig
else:
    from config.default import DefaultConfig

    config_obj = DefaultConfig


class Config(config_obj):
    pass
