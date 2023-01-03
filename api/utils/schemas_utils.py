from marshmallow import ValidationError


def validate_model_object_does_not_exist(
    Model, model_attribute, attribute_value, field_name=''
):
    """
    Check if a model object doesn't exists for marshmallow schema validation
    :param Model, model_attribute, attribute_value, field_name='':
    :Returns: None, Raise ValidationError if model object exists
    """

    error = None
    if attribute_value in ["", None]:
        error = f"{field_name} field is Empty. Enter a valid one."
    else:
        # Check if model_object exists
        obj = Model.query.filter(model_attribute == attribute_value).first()
        if obj is not None:
            error = f"{field_name} already exist."

    if error is not None:
        raise ValidationError(error, field_name=field_name)


def validate_model_object_does_exist(
    Model, model_attribute, attribute_value, field_name=''
):
    """
    Check if a model object exists for marshmallow schema validation
    :param Model, model_attribute, attribute_value, field_name='':
    :Returns: None, Raise ValidationError if model object exists
    """

    error = None
    if attribute_value in ["", None]:
        error = f"{field_name} field is Empty. Enter a valid one."
    else:
        # Check if model_object exists
        obj = Model.query.filter(model_attribute == attribute_value).first()
        if obj is None:
            error = f"{field_name} does not exist."

    if error is not None:
        raise ValidationError(error, field_name=field_name)


def validate_phone_number(number, min_length=10, max_length=15):
    """
    Check if a kenyan phone number provided has a max length of 13 (with country code inclusion)
    note: phone number length targets kenya, otherwise, this code needs update in the future.
    :param number, min_length=10, max_length=15:
    :Returns: None, Raise ValidationError if phone number is invalid.
    """

    number = str(number).replace("+", "")

    if not min_length <= len(number) <= max_length:
        raise ValidationError(
            f"Phone number must be between {min_length} and"
            f" {max_length} digits without spaces: {number}",
            field_name="phone_number"
        )

    try:
        int(number)
    except ValueError:
        raise ValidationError(
            f"Phone number invalid: {number}",
            field_name="phone_number"
        )
