import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

current_env = os.getenv("ENVIRONMENT", "production").lower()

if current_env == "production":
    from config.production import *
elif current_env == "staging": 
    from config.staging import *
elif current_env == "testing":
    from config.testing import *
elif current_env == "development":
    from config.development import *
else:
    from config.default import *
