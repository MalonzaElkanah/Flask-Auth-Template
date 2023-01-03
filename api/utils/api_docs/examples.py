spec_examples = {
    "register_user_success": {
        "message": 'User Created. Confirmation link has been sent to your email.',
        "data": {
            "email": "user@example.com",
            "phone_number": "string",
            "username": "string"
        },
        "status": 201
    },
    "register_user_error": {
        "data": {
            "confirm_password": "string123445",
            "email": "user@example.com",
            "password": "string123334"
        },
        "errors": {
            "confirm_password": [
              "Password and confirm password do not match"
            ]
        },
        "status": 400
    },
    "email_confirmed_success": {
        "message": "Email confirmed successfully!",
        "status": 200
    },
    "resend_user_email_confirm_success": {
        "data": {
            "email": "elkanahmalonza2@gmail.com"
        },
        "message": "Confirmation link sent to your Email.",
        "status": 200
    },
    "resend_user_email_confirm_error1": {
        "data": {
            "email": "elkanahmalonza3@gmail.com"
        },
        "errors": {
            "email": [
                "email does not exist."
            ]
        },
        "message": "",
        "status": 400
    },
    "resend_user_email_confirm_error": {
        "data": {
            "email": "elkanahmalonza1@gmail.com"
        },
        "message": "Your Email is already confirmed. Please login.",
        "status": 200
    },
    "login_success": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjcxNjk5OTc0LCJqdGkiOiIzYTIwNjNjMi00ZWZkLTQ5YzctYWU1OS1mM2YyODBhM2E3NTgiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiYTk5MWRiYzItNzU1OC0xMWVkLTllZDgtZmY0MjMxMjg0MDc3IiwibmJmIjoxNjcxNjk5OTc0LCJleHAiOjE2NzE3MDM1NzR9.fhyTFF8vZTkEkaCnYuaYtGPmJQ3UmCX4txRDl__mjnM",
        "message": "User logged-in successfully.",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MTY5OTk3NCwianRpIjoiMzljMTQ4MTctMzA3OC00NzI5LWE2ZWEtNDNkODdiYmRiODhlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJhOTkxZGJjMi03NTU4LTExZWQtOWVkOC1mZjQyMzEyODQwNzciLCJuYmYiOjE2NzE2OTk5NzQsImV4cCI6MTY3NDI5MTk3NH0.SY1-Lc_4LSFg4NSiq7RFR-Js0tSe4p3pNXtMAs2lhsY",
        "status": 200
    },
    "revoke_token_success": {
        "message": "User token revoked.",
        "status": 200
    },
    "refresh_token_success": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MTcwMDcxMiwianRpIjoiMDI4NjcyMWEtYmRiZi00ZTY4LWI4ZmMtNDFiMTlhNTRmN2FjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5OTFkYmMyLTc1NTgtMTFlZC05ZWQ4LWZmNDIzMTI4NDA3NyIsIm5iZiI6MTY3MTcwMDcxMiwiZXhwIjoxNjcxNzA0MzEyfQ.0MPhx28iJLGx01_IyAiQp7W1Rbs35Yyy4DkXlNzuyLg",
        "message": "New access token.",
        "status": 200
    },

    "token_expired": {
        "msg": "Token has expired"
    },
    "token_revoked": {
        "msg": "Token has been revoked"
    },
    "token_invalid": {
        "msg": "Signature verification failed"
    },
    "token_invalid2": {
        "msg": "Not enough segments"
    },

    "permission_error": {
        "message": "You don't have the permission!",
        "status": 403
    },

    "change_password_success": {
        "message": "Password changed successfully.\n Next time you login you will be required to enter the new password.",
        "status": 200
    },
    "forgot_password_request_success": {
        "data": {
            "email": "elkanahmalonza@gmail.com"
        },
        "message": "A link to change your password has been sent to your email.",
        "status": 200
    },
    "forgot_password_new_password_success": {
        "message": "Password changed successfully.\n Next time you login you will be required to enter the new password.",
        "status": 200
    },

    "user_profile_get_success": {
        "data": {
            "accounts": [
                {
                    "bio_data": "This is a test.",
                    "date_created": "2022-12-12T08:23:55.647523",
                    "date_modified": None,
                    "display_photo": "display_photo",
                    "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
                    "name": "Malone"
                }
            ],
            "email": "elkanahmalonza@gmail.com",
            "id": "a991dbc2-7558-11ed-9ed8-ff4231284077",
            "is_verified": "True",
            "phone_number": "0716504983",
            "roles": [
                {
                    "name": "Client"
                }
            ],
            "username": "malone"
        },
        "message": "Data fetched.",
        "status": 200
    },

    "user_profile_update_success": {
        "data": {
            "email": "elkanahmalonza@gmail.com",
            "phone_number": "0716504983",
            "username": "malone"
        },
        "message": "Your user profile has been updated!!",
        "status": 200
    },

    "user_lists_success": {
        "data": [
            {
                "accounts": [],
                "email": "elkanahmalonza1@gmail.com",
                "id": "b0fe25f6-81dc-11ed-b480-0dfc1f9c59f8",
                "is_verified": "True",
                "phone_number": "0700000000",
                "roles": [
                    {
                        "name": "Client"
                    }
                ],
                "username": "malonzajr"
            },
            {
                "accounts": [],
                "email": "elkanahmalonza2@gmail.com",
                "id": "dfa50aac-81df-11ed-839a-bb1a11c1fb89",
                "is_verified": "False",
                "phone_number": "0700000001",
                "roles": [
                    {
                        "name": "Client"
                    }
                ],
                "username": "malonza"
            },
            {
                "accounts": [
                    {
                        "bio_data": "This is a test.",
                        "date_created": "2022-12-12T08:23:55.647523",
                        "date_modified": None,
                        "display_photo": "display_photo",
                        "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
                        "name": "Malone"
                    }
                ],
                "email": "elkanahmalonza@gmail.com",
                "id": "a991dbc2-7558-11ed-9ed8-ff4231284077",
                "is_verified": "True",
                "phone_number": "0716504983",
                "roles": [
                    {
                        "name": "SuperAdmin"
                    },
                    {
                        "name": "Client"
                    }
                ],
                "username": "malone"
            },
            {
                "accounts": [],
                "email": "clienttest1@jmail.com",
                "id": "97439be0-7b84-11ed-98bb-a518d967d620",
                "is_verified": "False",
                "phone_number": "0722860535",
                "roles": [
                    {
                        "name": "Client"
                    }
                ],
                "username": "clienttest1"
            }
        ],
        "message": "Data fetched!",
        "status": 200
    },
    "user_detail_success": {
        "data": {
            "accounts": [
                {
                    "bio_data": "This is a test.",
                    "date_created": "2022-12-12T08:23:55.647523",
                    "date_modified": None,
                    "display_photo": "display_photo",
                    "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
                    "name": "Malone"
                }
            ],
            "email": "elkanahmalonza@gmail.com",
            "id": "a991dbc2-7558-11ed-9ed8-ff4231284077",
            "is_verified": "True",
            "phone_number": "0716504983",
            "roles": [
                {
                    "name": "SuperAdmin"
                },
                {
                    "name": "Client"
                }
            ],
            "username": "malone"
        },
        "message": "Data fetched!",
        "status": 200
    },

    "role_lists_success": {
        "data": [
            {
                "id": "55f7d18c-748c-11ed-aa36-1beace6c3a2c",
                "name": "SuperAdmin"
            },
            {
                "id": "5602ec3e-748c-11ed-aa36-1beace6c3a2c",
                "name": "Admin"
            },
            {
                "id": "56058e26-748c-11ed-aa36-1beace6c3a2c",
                "name": "Client"
            }
        ],
        "message": "Data fetched!",
        "status": 200
    },

    "role_create_success": {
        "data": {
            "id": "e63301ee-81e4-11ed-9d76-73174e16b677",
            "name": "moderator",
            "users": []
        },
        "message": "Role Created.",
        "status": 201
    },

    "role_detail_success": {
        "data": {
            "id": "56058e26-748c-11ed-aa36-1beace6c3a2c",
            "name": "Client",
            "users": [
                {
                    "email": "elkanahmalonza2@gmail.com",
                    "id": "dfa50aac-81df-11ed-839a-bb1a11c1fb89",
                    "is_verified": "False",
                    "phone_number": "0700000001",
                    "username": "malonza"
                },
                {
                    "email": "elkanahmalonza1@gmail.com",
                    "id": "b0fe25f6-81dc-11ed-b480-0dfc1f9c59f8",
                    "is_verified": "True",
                    "phone_number": "0700000000",
                    "username": "malonzajr"
                },
                {
                    "email": "clienttest1@jmail.com",
                    "id": "97439be0-7b84-11ed-98bb-a518d967d620",
                    "is_verified": "False",
                    "phone_number": "0722860535",
                    "username": "clienttest1"
                },
                {
                    "email": "elkanahmalonza@gmail.com",
                    "id": "a991dbc2-7558-11ed-9ed8-ff4231284077",
                    "is_verified": "True",
                    "phone_number": "0716504983",
                    "username": "malone"
                }
            ]
        },
        "message": "Data fetched!",
        "status": 200
    },

    "role_update_success": {
        "data": {
            "id": "e63301ee-81e4-11ed-9d76-73174e16b677",
            "name": "CustomerCare",
            "users": []
        },
        "message": "Role Updated!",
        "status": 200
    },

    "role_delete_success": {
        "message": "Role Deleted!",
        "status": 200
    },

    "accounts_lists_success": {
        "data": [
            {
                "bio_data": "This is a test.",
                "date_created": "2022-12-12T08:23:55.647523",
                "date_modified": None,
                "display_photo": "display_photo",
                "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
                "name": "Malone"
            }
        ],
        "message": "Data fetched!",
        "status": 200
    },

    "account_create_success": {
        "data": {
            "bio_data": "this is a test",
            "date_created": "2022-12-22T18:06:27.368028",
            "date_modified": None,
            "display_photo": "default-avatar.png",
            "id": "b32d6bb6-8222-11ed-bf5b-cd22d63f323e",
            "name": "test1"
        },
        "message": "Account Created.",
        "status": 201
    },

    "account_detail_success": {
        "data": {
            "bio_data": "This is a test.",
            "date_created": "2022-12-12T08:23:55.647523",
            "date_modified": None,
            "display_photo": "display_photo",
            "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
            "name": "Malone"
        },
        "message": "Data fetched!",
        "status": 200
    },
    "account_update_success": {
        "data": {
            "bio_data": "This is a test.",
            "date_created": "2022-12-12T08:23:55.647523",
            "date_modified": "2022-12-22T18:11:22.299965",
            "display_photo": "display_photo",
            "id": "222f64cc-79f6-11ed-80d3-6b0192736463",
            "name": "Malone101"
        },
        "message": "Account Updated!",
        "status": 200
    },
    "account_delete_success": {
        "message": "Account Deleted!",
        "status": 200
    }
}
