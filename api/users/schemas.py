from marshmallow import Schema, fields, validates, validate, ValidationError, validates_schema
from flask_jwt_extended import current_user

from api.models import User
from api.utils.schemas_utils import (
    validate_model_object_does_not_exist, validate_model_object_does_exist,
    validate_phone_number
)
from api.users.accounts.schemas import AccountSchema


class RoleSchema(Schema):
    name = fields.String()


class UserSchema(Schema):
    id = fields.String(attribute="uuid")
    username = fields.String()
    email = fields.Email()
    phone_number = fields.String()
    is_verified = fields.String(attribute="is_email_confirmed")
    roles = fields.Nested(RoleSchema, many=True)
    accounts = fields.Nested(AccountSchema, many=True)


class UserRegisterSchema(Schema):
    username = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "username is required"}
    )
    email = fields.Email(
        required=True,
        validate=[validate.Length(min=8, max=50)],
        error_messages={"required": "email is required"}
    )
    phone_number = fields.String(
        required=True,
        validate=[validate.Length(min=6, max=20)],
        error_messages={"required": "phone_number is required"}
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "password is required"}
    )
    confirm_password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "Confirm password is required"}
    )

    @validates("username")
    def validate_username(self, username):
        validate_model_object_does_not_exist(User, User.username, username, field_name='username')

    @validates("email")
    def validate_email(self, email):
        validate_model_object_does_not_exist(User, User.email, email, field_name='email')

    @validates("phone_number")
    def validate_phone_number(self, phone_number):
        validate_model_object_does_not_exist(
            User, User.phone_number, phone_number, field_name='phone_number'
        )
        validate_phone_number(phone_number)

    @validates("password")
    def validate_password(self, password):
        if password in ["", None]:
            raise ValidationError(
                "Password field is Empty. Enter a valid password.", field_name="password"
            )

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError(
                "Password and confirm password do not match", field_name="confirm_password"
            )


class UserEmailConfirmSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "email is required"}
    )

    @validates("email")
    def validate_email(self, email):
        validate_model_object_does_exist(User, User.email, email, field_name='email')


class UserLoginSchema(Schema):
    username = fields.String(
        required=True,
        error_messages={"required": "username is required"}
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "password is required"}
    )

    @validates("username")
    def validate_username(self, username):
        if username in ["", None]:
            raise ValidationError(
                "Username field is Empty. Enter a valid username.", field_name="username"
            )
        else:
            # Check if username exists
            user = User.query.filter_by(username=username).one_or_none()
            if user is None:
                raise ValidationError(
                    "Invalid Username or Password.", field_name="password"
                )

    @validates("password")
    def validate_password(self, password):
        if password in ["", None]:
            raise ValidationError(
                "Password field is Empty. Enter a valid password.", field_name="password"
            )


class UserRevokeTokenSchema(Schema):
    token = fields.String(
        required=True,
        error_messages={"required": "token is required"}
    )

    @validates("token")
    def validate_token(self, token):
        if token in ["", None]:
            raise ValidationError(
                "Token is Empty. Enter a valid token.", field_name="token"
            )
        else:
            # Check if token is valid
            user = User.verify_auth_token(token)
            if user is None:
                raise ValidationError(
                    "Token is invalid.", field_name="token"
                )

            if user.auth_token is None or token != user.auth_token:
                raise ValidationError(
                    "Token is invalid.", field_name="token"
                )


class UserChangePasswordSchema(Schema):
    current_password = fields.String(
        required=True,
        error_messages={"required": "current_password is required"}
    )
    new_password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "new_password is required"}
    )
    confirm_password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "confirm_password is required"}
    )

    @validates("current_password")
    def validate_current_password(self, current_password):
        if current_password in ["", None]:
            raise ValidationError(
                "Current Password field is Empty. Enter a valid password.",
                field_name="current_password"
            )
        else:
            user = current_user
            if user:
                if not user.verify_password(current_password):
                    raise ValidationError(
                        "Current Password is incorrect.", field_name="current_password"
                    )
            else:
                raise ValidationError(
                        "User is not logged in.", field_name="current_password"
                    )

    @validates("new_password")
    def validate_new_password(self, new_password):
        if new_password in ["", None]:
            raise ValidationError(
                "New Password field is Empty. Enter a valid password.",
                field_name="new_password"
            )

    @validates("confirm_password")
    def validate_confirm_password(self, confirm_password):
        if confirm_password in ["", None]:
            raise ValidationError(
                "Confirm Password field is Empty. Enter a valid password.",
                field_name="confirm_password"
            )

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get("new_password") != data.get("confirm_password"):
            raise ValidationError(
                "New Password and confirm password do not match", field_name="confirm_password"
            )
        elif data.get("current_password") == data.get("new_password"):
            raise ValidationError(
                "Current Password is same as new password.", field_name="new_password"
            )


class UserForgotPasswordSchema(Schema):
    new_password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "new_password is required"}
    )
    confirm_password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8)],
        error_messages={"required": "confirm_password is required"}
    )

    @validates("new_password")
    def validate_new_password(self, new_password):
        if new_password in ["", None]:
            raise ValidationError(
                "New Password field is Empty. Enter a valid password.",
                field_name="new_password"
            )

    @validates("confirm_password")
    def validate_confirm_password(self, confirm_password):
        if confirm_password in ["", None]:
            raise ValidationError(
                "Confirm Password field is Empty. Enter a valid password.",
                field_name="confirm_password"
            )

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get("new_password") != data.get("confirm_password"):
            raise ValidationError(
                "New Password and confirm password do not match", field_name="confirm_password"
            )


class UserUpdateSchema(Schema):
    username = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "username is required"}
    )
    email = fields.Email(
        required=True,
        validate=[validate.Length(min=8, max=50)],
        error_messages={"required": "email is required"}
    )
    phone_number = fields.String(
        required=True,
        validate=[validate.Length(min=6, max=20)],
        error_messages={"required": "phone_number is required"}
    )

    @validates("username")
    def validate_username(self, username):
        if username != current_user.username:
            validate_model_object_does_not_exist(
                User,
                User.username,
                username,
                field_name='username'
            )

    @validates("email")
    def validate_email(self, email):
        if email != current_user.email:
            validate_model_object_does_not_exist(
                User,
                User.email,
                email,
                field_name='email'
            )

    @validates("phone_number")
    def validate_phone_number(self, phone_number):
        if phone_number != current_user.phone_number:
            validate_model_object_does_not_exist(
                User,
                User.phone_number,
                phone_number,
                field_name='phone_number'
            )
            validate_phone_number(phone_number)
