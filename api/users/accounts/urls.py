from api.users.accounts.views import AccountDetailViewAPI, AccountViewAPI


def accounts_urls(api):
    api.add_resource(
        AccountViewAPI,
        '/v1/user/me/accounts',
        "/v1/user/me/accounts/",
        endpoint="user_accounts_api"
    )
    api.add_resource(
        AccountDetailViewAPI,
        '/v1/user/me/accounts/<string:account_id>',
        "/v1/user/me/accounts/<string:account_id>/",
        endpoint="user_accounts-detail_api"
    )
