from api.users.views import (
    UserRegisterViewAPI, UserConfirmEmailViewAPI,
    UserLoginViewAPI, UserLogoutViewAPI, UserRefreshTokenViewAPI,
    UserChangePasswordViewAPI, UserForgotPasswordViewAPI, MyUserProfileViewAPI,
    UserViewAPI, UserDetailViewAPI, FileUploadsView,
)


def user_urls(api):
    api.add_resource(
        UserRegisterViewAPI,
        '/v1/user/register',
        "/v1/user/register/",
        endpoint="user_register_api"
    )
    api.add_resource(
        UserConfirmEmailViewAPI,
        '/v1/user/confirm-email',
        "/v1/user/confirm-email/",
        endpoint="user_confirm-email_api"
    )
    api.add_resource(
        UserLoginViewAPI,
        '/v1/user/login',
        "/v1/user/login/",
        endpoint="user_login_api"
    )
    api.add_resource(
        UserRefreshTokenViewAPI,
        '/v1/user/refresh',
        "/v1/user/refresh/",
        endpoint="user_token_refresh_api"
    )
    api.add_resource(
        UserLogoutViewAPI,
        '/v1/user/logout',
        "/v1/user/logout/",
        endpoint="user_logout_api"
    )
    api.add_resource(
        UserChangePasswordViewAPI,
        '/v1/user/change-password',
        "/v1/user/change-password/",
        endpoint="user_change-password_api"
    )
    api.add_resource(
        UserForgotPasswordViewAPI,
        '/v1/user/forgot-password',
        "/v1/user/forgot-password/",
        endpoint="user_forgot-password_api"
    )

    api.add_resource(
        MyUserProfileViewAPI,
        '/v1/user/me',
        "/v1/user/me/",
        endpoint="user_profile_api"
    )

    api.add_resource(
        UserViewAPI,
        '/v1/users',
        "/v1/users/",
        endpoint="user_list_api"
    )
    api.add_resource(
        UserDetailViewAPI,
        '/v1/users/<string:user_id>',
        "/v1/users/<string:user_id>/",
        endpoint="user_detail_api"
    )

    api.add_resource(
        FileUploadsView,
        '/v1/users/<string:file_name>',
        "/v1/users/<string:file_name>/",
        endpoint="uploaded_file"
    )
