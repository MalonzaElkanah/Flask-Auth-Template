spec_parameters = {
    "confirm_token": {
        "name": "token",
        "in": "query",
        "description": "token to confirm email",
        "required": 'true',
        "schema": {
            "type": "string"
        },
        "style": "simple"
    },
    "user_id": {
        "name": "user_id",
        "in": "path",
        "description": "user to fetch",
        "required": 'true',
        "schema": {
            "type": "string"
        }
    },
    "role_id": {
        "name": "role_id",
        "in": "path",
        "description": "fetch role details",
        "required": 'true',
        "schema": {
            "type": "string"
        }
    },
    "account_id": {
        "name": "account_id",
        "in": "path",
        "description": "fetch role details",
        "required": 'true',
        "schema": {
            "type": "string"
        }
    },
}
