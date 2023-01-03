from marshmallow import Schema, fields, validate

from api.users.schemas import (
    UserRegisterSchema, UserEmailConfirmSchema, UserLoginSchema, UserRevokeTokenSchema,
    UserChangePasswordSchema, UserForgotPasswordSchema, UserSchema, UserUpdateSchema,
)
from api.users.accounts.schemas import AccountUpdateSchema


class GeneralResponseSchema(Schema):
    status = fields.Integer(
        default=200,
        validate=[validate.Range(min=100, max=600)],
    )
    message = fields.String(
        default="Success."
    )
    data = fields.Dict(
        keys=fields.String(),
        values=fields.String()
    )


class GeneralErrorSchema(Schema):
    status = fields.Integer(
        default=400,
        validate=[validate.Range(min=100, max=600)],
    )
    message = fields.String(
        default="This is an error message."
    )


class ValidationErrorSchema(Schema):
    status = fields.Integer(
        default=400,
        validate=[validate.Range(min=100, max=600)],
    )
    message = fields.String(
        default="Please correct the errors"
    )
    errors = fields.Dict(
        keys=fields.String(),
        values=fields.List(fields.String())
    )
    data = fields.Dict(
        keys=fields.String(),
        values=fields.String()
    )


class RoleDetailSchema(Schema):
    id = fields.String(attribute="uuid")
    name = fields.String(
        required=True,
        validate=[validate.Length(max=50)],
        error_messages={"required": "name is required"}
    )
    users = fields.Nested(UserSchema, exclude=["roles", "accounts"], many=True)


marshmallow_schemas = [
    UserRegisterSchema, UserEmailConfirmSchema, UserLoginSchema, UserRevokeTokenSchema,
    UserChangePasswordSchema, UserForgotPasswordSchema, UserSchema, UserUpdateSchema,
    AccountUpdateSchema,
    RoleDetailSchema,
    GeneralResponseSchema, GeneralErrorSchema, ValidationErrorSchema,
]
