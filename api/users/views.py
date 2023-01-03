from flask import request, url_for, current_app, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_jwt,
    jwt_required, current_user
)
from marshmallow import ValidationError

from api.users.schemas import (
    UserRegisterSchema, UserEmailConfirmSchema, UserLoginSchema,
    UserChangePasswordSchema, UserForgotPasswordSchema, UserSchema, UserUpdateSchema
)
from api.models import User, Role, TokenBlocklist
from api.utils import db, token
from api.utils.views_utils import role_required, json_response

from datetime import timezone, datetime
import uuid


class UserRegisterViewAPI(Resource):

    def post(self):
        """
        This Create a user that will have access to application
        ---
        tags:
          - users
        requestBody:
          description: user to add to the application
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRegister'
        responses:
          '200':
            description: User created Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/register_user_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            result = UserRegisterSchema().load(request.get_json())
            result.pop('confirm_password')
        except ValidationError as error:

            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        user = User(**result, uuid=uuid.uuid1())
        user.set_password(user.password)
        user.set_email_confirm_token(user.email)

        role = Role.query.filter_by(name='Client').one_or_none()

        if role:
            role.users.append(user)
        else:
            role = Role(name="Client")
            role.users.append(user)
            db.session.add(role)
            db.session.commit()

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=result['email']).one_or_none()

        if user:
            message = f'''
                Thank you for signing up with SpaceYaTech.
                Please click this
                <a href="{url_for("user_confirm-email_api")}?token={user.email_confirm_token}">
                link to confirm your email</a>
            '''
            print(message)

            # TODO:
            # Send Actual Email
            # Confirm Phone number via OTP

            return json_response(
                status=201,
                data=UserRegisterSchema().dump(result),
                message=f"""User Created. Confirmation link has been sent to your email.
                Verify you email to login. If no confirmation link please click this
                <a href="{url_for('user_confirm-email_api')}"> link to resend the link</a>."""
            )
        else:

            return json_response(
                status=500,
                data=UserRegisterSchema().dump(result),
                message="Error Creating user. Please try again later."
            )


class UserConfirmEmailViewAPI(Resource):

    def get(self):
        """
        This will confirm/verify a user email to have access to application
        ---
        tags:
          - users
        responses:
          '200':
            description: Email confirmed Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/email_confirmed_success'
          '401':
            $ref: '#/components/responses/TokenInvalid'
          '404':
            $ref: '#/components/responses/GeneralError'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
        - $ref: '#/components/parameters/confirm_token'
        """

        str_token = request.args.get('token', None)

        if str_token:
            payload = token.decode(str_token, current_app.config["EMAIL_TOKEN_SECRET_KEY"])

            if 'error' in payload:
                return json_response(
                    status=401,
                    message=payload['error']
                )

            email = payload['data']

            user = User.query.filter_by(email=email).first()

            if not user:

                return json_response(
                    status=404,
                    message="User is not found!"
                )

            if user.email_confirm_token != str_token or user.email_confirm_token is None:

                return json_response(
                    status=401,
                    message="Token has been expired!"
                )

            user.is_email_confirmed = True
            user.email_confirm_token = None

            db.session.add(user)
            db.session.commit()

            return json_response(
                status=200,
                message="Email confirmed successfully!"
            )

    def post(self):
        """
        This will resend confirmation link to unverified user
        ---
        tags:
          - users
        requestBody:
          description: email of unconfirmed user application
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserEmailConfirm'
        responses:
          '200':
            description: User confirmation Link sent Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/resend_user_email_confirm_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            results = UserEmailConfirmSchema().load(request.get_json())
        except ValidationError as error:
            return json_response(
                status=400,
                errors=error.messages,
                data=request.get_json()
            )

        email = results.get("email")
        user = User.query.filter_by(email=email).one_or_none()
        if user:
            if not user.is_email_confirmed:
                user.set_email_confirm_token(user.email)
                db.session.commit()
                message = f'''
                Thank you for signing up with Space Ya Tech.
                Please click this link to confirm your email:
                {url_for("user_confirm-email_api")}?token={user.email_confirm_token}
                '''
                print(message)

                # TODO:
                # Send Actual Email

                return json_response(
                    status=200,
                    message="Confirmation link sent to your Email.",
                    data=request.get_json()
                )

            else:
                return json_response(
                    status=200,
                    message="Your Email is already confirmed. Please login.",
                    data=request.get_json()
                )

        else:
            return json_response(
                status=400,
                errors={"email": ["No user with that email found,"]},
                message="Error: Email does not exist.",
                data=request.get_json()
            )


class UserLoginViewAPI(Resource):

    def post(self):
        """
        This will send a authentication token to user
        ---
        tags:
          - users
          - auth
        requestBody:
          description: name and password of existing application user
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserLogin'
        responses:
          '200':
            description: Token Issued
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/login_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '403':
            $ref: '#/components/responses/UserNotConfirmed'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            results = UserLoginSchema().load(request.get_json())
        except ValidationError as error:
            return json_response(
                status=400,
                errors=error.messages,
                message="Fix this errors",
            )

        if results.get("username", None):
            user = User.query.filter_by(username=results["username"]).one_or_none()

            if user is not None:
                if user.is_email_confirmed:
                    if user.verify_password(results["password"]):
                        access_token = create_access_token(identity=user.uuid, fresh=True)
                        refresh_token = create_refresh_token(identity=user.uuid)

                        user.auth_token = access_token

                        db.session.add(user)
                        db.session.commit()

                        return json_response(
                            status=200,
                            refresh_token=refresh_token,
                            access_token=access_token,
                            message="User logged-in successfully."
                        )
                    else:
                        return json_response(
                            status=403, message="Wrong email or password"
                        )

                else:
                    return json_response(
                        status=403,
                        message=f"""
                        Your email is not Confirmed. Comfirmation Link was sent to your Email.
                        Click this <a href="{url_for('user_confirm-email_api')}">link to resend </a>
                        confirmation link.
                        """
                    )

        return json_response(
            status=403, message="Wrong email or password"
        )


class UserRefreshTokenViewAPI(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """
        Endpoint to send a new access token to user if valid refresh token provided
        ---
        tags:
          - users
          - auth
        security:
          - bearer_refresh_token: []
        responses:
          '200':
            description: Token Issued
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/refresh_token_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '403':
            $ref: '#/components/responses/UserNotConfirmed'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        identity = get_jwt_identity()

        if identity is not None:
            access_token = create_access_token(identity=identity, fresh=False)
            # identity.auth_token = access_token

            # db.session.add(identity)
            # db.session.commit()

            return json_response(
                status=200,
                access_token=access_token,
                message="New access token."
            )

        return json_response(
            status=403, message="Invalid Refresh Token."
        )


class UserLogoutViewAPI(Resource):

    @jwt_required()
    def delete(self):
        """
        Endpoint for revoking the current users access token.
        ---
        tags:
          - users
          - auth
        security:
          - bearer_token: []
        responses:
          '200':
            description: User token revoked
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/revoke_token_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        # Saved the unique identifier (jti) for the JWT into our database.

        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return json_response(
            status=200, message="User token revoked."
        )


class UserChangePasswordViewAPI(Resource):

    @jwt_required()
    def put(self):
        """
        This endpoint will change user password
        ---
        tags:
          - users
        security:
          - bearer_token: []
        requestBody:
          description: request to change user password
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserChangePassword'
        responses:
          '200':
            description: Password changed successfully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/change_password_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            results = UserChangePasswordSchema().load(request.get_json())
        except ValidationError as error:
            return json_response(
                status=400,
                message="Fix this errors!",
                errors=error
            )

        password = results.get("current_password")
        new_password = results.get("new_password")

        # validate old password
        user = current_user
        if user:
            if user.verify_password(password):
                user.set_password(new_password)
                db.session.commit()

                return json_response(
                    status=200,
                    message="""Password changed successfully.
                    Next time you login you will be required to enter the new password."""
                )
            else:
                return json_response(status=400, message="Wrong password")

        else:
            return json_response(
                status=403,
                message="""Error: You require to be logged in to change password."""
            )


class UserForgotPasswordViewAPI(Resource):

    def put(self):
        """
        This endpoint is for changing the user password after the user has forgotten.
        ---
        tags:
          - users
        requestBody:
          description: request to send new user password
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserForgotPassword'
        responses:
          '200':
            description: Password Changed Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/forgot_password_new_password_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenInvalid'
          '500':
            $ref: '#/components/responses/GeneralError'
        parameters:
        - $ref: '#/components/parameters/confirm_token'
        """

        str_token = request.args.get('token', None)

        if str_token:
            payload = token.decode(str_token, current_app.config["EMAIL_TOKEN_SECRET_KEY"])

            if 'error' in payload:
                return json_response(
                    status=401,
                    message=payload['error']
                )

            uuid = payload['data']

            try:
                results = UserForgotPasswordSchema().load(request.get_json())
            except ValidationError as error:
                return json_response(
                    status=400, errors=error, data=request.get_json()
                )

            user = User.query.filter_by(uuid=uuid).one_or_none()
            if user:
                new_password = results.get("new_password")
                user.set_password(new_password)
                db.session.commit()

                return json_response(
                    status=200,
                    message="""Password changed successfully.
                    Next time you login you will be required to enter the new password."""
                )

        return json_response(
            status=401,
            message="User is not found or Maybe token has expired!"
        )

    def post(self):
        """
        This endpoint is for requesting password reset link to be sent to user email
        after the user has forgotten the password.
        ---
        tags:
          - users
        requestBody:
          description: request to send password reset link
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserEmailConfirm'
        responses:
          '200':
            description: Password Reset link sent Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/forgot_password_request_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '403':
            $ref: '#/components/responses/UserNotConfirmed'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            results = UserEmailConfirmSchema().load(request.get_json())
        except ValidationError as error:
            return json_response(status=400, errors=error, data=request.get_json())

        email = results.get("email")
        user = User.query.filter_by(email=email).one_or_none()
        if user:
            if user.is_email_confirmed:
                user.set_forgot_password_token(user.uuid)
                db.session.commit()
                message = f'''
                Please find a link to change your password.
                The link will expire in 30 minutes: <a href="
                {url_for("user_forgot-password_api")}?token={user.email_confirm_token}">
                Link to change your password</a>
                '''
                # send_email(message, recipients=[email,])
                print(f"email: {message}")
            else:
                return json_response(
                    status=403,
                    message=f"""
                    Your email is not Confirmed. Comfirmation Link was sent to your Email.
                    Click this <a href="{url_for('user_confirm-email_api')}">link to resend </a>
                    confirmation link.
                    """
                )

        return json_response(
            status=200,
            message="A link to change your password has been sent to your email.",
            data=request.get_json()
        )


class MyUserProfileViewAPI(Resource):

    @jwt_required()
    def get(self):
        """
        This endpoint returns the logged users profile
        ---
        tags:
          - users
        security:
          - bearer_token: []
        responses:
          '200':
              description: my user profile to be returned
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        $ref: '#/components/schemas/User'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/user_profile_get_success'

          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
        """

        user = current_user

        return json_response(
            status=200,
            message="Data fetched.",
            data=UserSchema().dump(user)
        )

    @jwt_required()
    def put(self):
        """
        This endpoint is for updating your user profile.
        ---
        tags:
          - users
        security:
          - bearer_token: []
        requestBody:
          description: request to send user profile update
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserUpdate'
        responses:
          '200':
            description: Profile Updated Succefully
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/GeneralResponse'
                example:
                  $ref: '#/components/examples/user_profile_update_success'
          '400':
            $ref: '#/components/responses/ValidationError'
          '401':
            $ref: '#/components/responses/TokenMissing'
          '500':
            $ref: '#/components/responses/GeneralError'
        """

        try:
            result = UserUpdateSchema().load(request.get_json())
        except ValidationError as error:
            return json_response(
                status=400,
                message="Please correct the errors",
                errors=error.messages
            )

        user = current_user

        username = result["username"]
        email = result["email"]
        phone_number = result["phone_number"]

        if username != user.username:
            user.username = username

        if email != user.email:
            user.email = email
            user.set_email_confirm_token(email)
            user.is_email_confirmed = True
            message = f'''
                Thank you for being a valued member of SpaceYaTech.
                Please click this
                <a href="{url_for("user_confirm-email_api")}?token={user.email_confirm_token}">
                link to confirm the new email</a>
            '''
            # TODO:
            # Send the actual email
            print(message)

        if phone_number != user.phone_number:
            user.phone_number = phone_number
            # TODO:
            # Confirm Phone number via OTP

        db.session.commit()

        if not user.is_email_confirmed:
            return json_response(
                    status=200,
                    message=f"""
                    Your user profile has been updated!!
                    We have noticed that you have changed the email address.
                    Comfirmation Link was sent to the new Email.
                    Click this <a href="{url_for('user_forgot-password_api')}">link to resend </a>
                    confirmation link.
                    """,
                    data=request.get_json()
                )

        return json_response(
            status=200,
            message="Your user profile has been updated!!",
            data=request.get_json()
        )


class UserViewAPI(Resource):

    @jwt_required()
    @role_required(['Admin', 'SuperAdmin'])
    def get(self):
        """
        This endpoint lists all users in application
        ---
        tags:
          - users
          - admin
        security:
          - bearer_token: []
        responses:
          '200':
              description: user list returned
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        type: array
                        items:
                          $ref: '#/components/schemas/User'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/user_lists_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
          '403':
              $ref: '#/components/responses/AccessDenied'
        """

        users = User.query.all()

        return json_response(
            status=200,
            message="Data fetched!",
            data=UserSchema(many=True).dump(users)
        )


class UserDetailViewAPI(Resource):

    @jwt_required()
    @role_required(['Admin', 'SuperAdmin'])
    def get(self, user_id):
        """
        This endpoint returns detailed data of a users
        ---
        tags:
          - users
          - admin
        security:
          - bearer_token: []
        responses:
          '200':
              description: my user profile to be returned
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      data:
                        $ref: '#/components/schemas/User'
                      status:
                        type: integer
                        minimum: 100
                        maximum: 600
                  example:
                    $ref: '#/components/examples/user_detail_success'
          '401':
              $ref: '#/components/responses/TokenMissing'
          '400':
              $ref: '#/components/responses/TokenInvalid'
          '403':
              $ref: '#/components/responses/AccessDenied'
          '404':
              $ref: '#/components/responses/NotFound'
        parameters:
          - $ref: '#/components/parameters/user_id'
        """

        user = User.query.filter_by(uuid=user_id).one_or_none()

        if user:
            return json_response(
                status=200,
                message="Data fetched!",
                data=UserSchema().dump(user)
            )
        else:
            return json_response(
                status=404,
                message="User not Found.",
                errors="User not Found"
            )


class FileUploadsView(Resource):

    def get(self, file_name):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], file_name)
