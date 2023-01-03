from api.users.roles.views import RolesDetailViewAPI, RolesViewAPI


def roles_urls(api):
    api.add_resource(
        RolesViewAPI,
        '/v1/user/roles',
        "/v1/user/roles/",
        endpoint="user_roles_api"
    )
    api.add_resource(
        RolesDetailViewAPI,
        '/v1/user/roles/<string:role_id>',
        "/v1/user/roles/<string:role_id>/",
        endpoint="user_roles-detail_api"
    )
