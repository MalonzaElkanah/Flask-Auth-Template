from api.utils import create_app
from api.urls import api_urls


app = create_app('config', name="Main")

# Register Urls
api_urls(app)
