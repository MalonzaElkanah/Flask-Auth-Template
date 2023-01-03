from flask import g, redirect, url_for, jsonify, request, current_app
from flask_jwt_extended import current_user

import functools

from api.utils.token import decode
from api.utils.application_data import ALLOWED_EXTENSIONS
from api.models import User


def json_response(status=200, message="", **kwargs):
    if status == 204:
        response = "", 204
    else:
        response = jsonify(status=status, message=message, **kwargs)
        response.status_code = status

    return response


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('user_login'))

        return view(*args, **kwargs)

    return wrapped_view


def token_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')

        if not token:
            return json_response(
                status=401,
                message="Token is required"
            )

        try:
            token = token.split("Bearer ")[1]
            data = decode(token, current_app.config["SECRET_KEY"])
            if data.get('data', None):
                uuid = data.get('data')
                user = User.query.filter_by(uuid=uuid).one_or_none()

                if user.auth_token is None:
                    return json_response(
                        status=400,
                        message="Token has been expired!"
                    )
                g.user = user
            else:
                return json_response(
                    status=400,
                    message=data.get('error', "Token is invalid!")
                )
        except Exception as e:
            print("error", e)
            return json_response(
                status=400,
                message="Token is invalid."
            )

        return view(*args, **kwargs)

    return wrapped_view


def role_required(roles):

    def decorated_function(f):

        @functools.wraps(f)
        def wrapped_view(*args, **kwargs):

            user = current_user

            if user is None:
                return json_response(
                    status=404,
                    message="User not found"
                )

            user_roles = user.roles

            if user_roles == []:
                return json_response(
                    status=403,
                    message="Access denied"
                )

            for role in user_roles:
                if role.name in roles:
                    return f(*args, **kwargs)

            return json_response(
                status=403,
                message="You don't have the permission!"
            )

        return wrapped_view

    return decorated_function


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
