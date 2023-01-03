from api.users.urls import user_urls
from api.users.roles.urls import roles_urls
from api.users.accounts.urls import accounts_urls


def api_urls(api):
    user_urls(api)
    roles_urls(api)
    accounts_urls(api)
