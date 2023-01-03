from marshmallow import Schema, fields, validate, validates

from api.utils.schemas_utils import validate_model_object_does_not_exist
from api.models import Account


class AccountSchema(Schema):
    name = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "name is required"}
    )
    bio_data = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=1500)],
        error_messages={"required": "bio_data is required"}
    )
    display_photo = fields.String()
    id = fields.String(attribute="uuid")
    date_created = fields.DateTime()
    date_modified = fields.DateTime()

    @validates("name")
    def validate_name(self, name):
        validate_model_object_does_not_exist(
            Account, Account.name, name, field_name='name'
        )


class AccountUpdateSchema(Schema):
    name = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "name is required"}
    )
    bio_data = fields.String(
        required=True,
        validate=[validate.Length(min=3, max=1500)],
        error_messages={"required": "bio_data is required"}
    )
    display_photo = fields.String()
