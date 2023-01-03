from marshmallow import Schema, fields, validate, validates

from api.utils.schemas_utils import validate_model_object_does_not_exist
from api.users.schemas import UserSchema
from api.models import Role


class RoleSchema(Schema):
    id = fields.String(attribute="uuid")
    name = fields.String(
        required=True,
        validate=[validate.Length(max=50)],
        error_messages={"required": "name is required"}
    )
    users = fields.Nested(UserSchema, exclude=["roles", "accounts"], many=True)

    @validates("name")
    def validate_name(self, name):
        validate_model_object_does_not_exist(
            Role, Role.name, name, field_name='name'
        )
