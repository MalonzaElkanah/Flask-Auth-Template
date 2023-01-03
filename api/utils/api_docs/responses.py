spec_responses = {
    "ValidationError": {
        "description": "Data Validation Error.",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/ValidationError"
                }
            }
        }
    },

    "NotFound": {
        "description": "Entity not found.",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/GeneralError"
                },
                "example": {
                    "message": "Entity not found.",
                    "status": 404
                }
            }
        }
    },

    "TokenMissing": {
        "description": "Token is missing in request.",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/GeneralError"
                },
                "example": {
                    "message": "Token is required",
                    "status": 401
                }
            }
        }
    },

    "TokenInvalid": {
        "description": "Token is invalid or expired.",
        "content": {
            "application/json": {
                "schema": {
                   "$ref": "#/components/schemas/GeneralError"
                },
                "example": {
                    "msg": "Token has been revoked"
                }
            }
        }
    },
    "AccessDenied": {
        "description": "Access Denied.",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/GeneralError"
                },
                "example": {
                    "message": "You don't have the permission",
                    "status": 403
                }
            }
        }
    },
    "UserNotConfirmed": {
        "description": "User email is not Confirmed.",
        "content": {
            "application/json": {
                "schema": {
                   "$ref": "#/components/schemas/GeneralError"
                },
                "example": {
                    "message": "Your email is not Confirmed. Comfirmation Link was sent to your Email.",
                    "status": 403
                }
            }
        }
    },
    "GeneralError": {
        "description": "General Error",
        "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/GeneralError"
              }
            }
        }
    }
}
