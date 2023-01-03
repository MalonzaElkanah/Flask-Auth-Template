import json

import pytest
from flask import url_for

from api.models import User
from tests.utils import create_user, generate_username, generate_number


@pytest.fixture(scope="module")
def unconfirmed_client_user(test_db, test_client, client_role):
    """Unconfirmed Test Client"""

    user = create_user(client_role)
    user.is_email_confirmed = False

    username = user.username

    test_db.session.add(user)
    test_db.session.commit()

    user = User.query.filter_by(username=username).one_or_none()

    return user


def test_user_registration(test_db, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_register_api' is posted to (POST)
    THEN check the response is valid and user created
    """

    data = {
        "email": "clienttest1@gmail.com",
        "username": "clienttest1",
        "phone_number": "1234567890",
        "password": "password",
        "confirm_password": "password",
    }
    initial_user_count = User.query.count()
    response = test_client.post(
        url_for("user_register_api"),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 201
    assert response.get_json().get("status") == 201
    assert "User Created." in response.get_json().get("message")
    assert User.query.count() == initial_user_count + 1

    user = User.query.filter_by(email=data["email"]).one_or_none()

    assert not user.is_email_confirmed


def test_user_registration_validation(test_db, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_register_api' url is posted to with invalid email (POST)
    THEN check an error message is returned to the user and user not created
    """

    data = {
        "email": "bad.email.com",
        "username": "username",
        "phone_number": "1234567890",
        "password": "password",
    }
    response = test_client.post(
        url_for("user_register_api"),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 400
    assert response.get_json().get("status") == 400
    assert "email address" in str(response.get_json())
    assert User.query.filter_by(email=data["email"]).one_or_none() is None


def test_resend_confirmation_email(test_client, unconfirmed_client_user):
    """
    GIVEN a Flask application configured for testing and unconfirmed user
    WHEN the 'user_confirm-email_api' is posted with unconfirmed user email (POST)
    THEN check the response is valid
    """

    response = test_client.post(
        url_for("user_confirm-email_api"),
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps({"email": unconfirmed_client_user.email})
    )

    print(response.get_json())
    assert response.status_code == 200
    assert "Confirmation link sent to your Email." in response.get_json()["message"]


def test_email_confirmation(test_db, test_client, unconfirmed_client_user):
    """
    GIVEN a Flask application configured for testing and unconfirmed user
    WHEN the 'user_confirm-email_api' is requested with email_confirm_token as parameter (GET)
    THEN check the response is valid and user is confirmed
    """

    assert not unconfirmed_client_user.is_email_confirmed
    assert unconfirmed_client_user.email_confirm_token is not None

    response = test_client.get(
        url_for("user_confirm-email_api", token=unconfirmed_client_user.email_confirm_token)
    )

    assert response.status_code == 200
    assert b"Email confirmed" in response.get_data()
    assert unconfirmed_client_user.is_email_confirmed and unconfirmed_client_user.email_confirm_token is None


def test_user_login_logout(test_db, test_client, client_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_login_api' is posted to (POST)
    THEN check the response is valid
    """

    data = {"username": client_user.username, "password": "password"}

    response = test_client.post(
        url_for("user_login_api"),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert "User logged-in" in response.get_json()["message"]
    assert "access_token" in response.get_json()
    assert "refresh_token" in response.get_json()

    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_logout_api' page is posted (POSTED)
    THEN check the response is valid and if revoke token can be used
    """

    token = client_user.auth_token

    response = test_client.delete(
        url_for("user_logout_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
    )

    assert response.status_code == 200
    assert "User token revoked." in response.get_json()["message"]

    response = test_client.get(
        url_for("user_profile_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401
    assert b"Data fetched." not in response.get_data()


def test_invalid_login(test_client, client_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_login_api' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """

    data = {"username": client_user.username, "password": "invalid_password"}

    response = test_client.post(
        url_for("user_login_api"),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 403
    assert response.get_json().get("status") == 403
    assert "Wrong email or password" in response.get_json()["message"]
    assert "access_token" not in response.get_json()


def test_refresh_token(test_client, client_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'user_token_refresh_api' is posted to (POST) with refresh token
    THEN check the response is valid
    """

    # Get access and refresh token
    data = {"username": client_user.username, "password": "password"}

    response = test_client.post(
        url_for("user_login_api"),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()
    assert "refresh_token" in response.get_json()

    access_token = response.get_json()["access_token"]
    refresh_token = response.get_json()["refresh_token"]

    # Test if Access token authenticates
    response = test_client.get(
        url_for("user_profile_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched." in response.get_data()

    # Fetch new access token
    response = test_client.post(
        url_for("user_token_refresh_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {refresh_token}",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()
    assert "New access token" in response.get_json()["message"]

    access_token = response.get_json()["access_token"]

    # Test the new access token
    response = test_client.get(
        url_for("user_profile_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched." in response.get_data()


def test_user_change_password(test_db, test_client, client_user):
    """
    GIVEN a Flask application configured for testing and a user
    WHEN the 'user_change-password_api' is posted to (PUT)
    THEN check the response is valid
    """

    data = {
        "current_password": "password",
        "new_password": "newpassword",
        "confirm_password": "newpassword",
    }

    client_user.set_auth_token(client_user.uuid)

    response = test_client.put(
        url_for("user_change-password_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert "Password changed successfully." in response.get_json()["message"]
    assert client_user.verify_password(data["new_password"])


def test_request_password_reset(test_client, client_user):
    """
    GIVEN a Flask application configured for testing and a user
    WHEN the 'user_forgot-password_api' is posted to (POST)
    THEN check the response is valid
    """

    response = test_client.post(
        url_for("user_forgot-password_api"),
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps({"email": client_user.email})
    )

    assert response.status_code == 200
    assert "A link to change your password has been sent to your email." in response.get_json()["message"]

    """
    GIVEN a Flask application configured for testing and a user
    WHEN the 'user_forgot-password_api' with change_password token as parameter  is posted to (PUT)
    THEN check the response is valid and password has changed
    """

    data = {
        "new_password": "newpassword",
        "confirm_password": "newpassword"
    }

    response = test_client.put(
        url_for("user_forgot-password_api", token=client_user.email_confirm_token),
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert "Password changed successfully." in response.get_json()["message"]
    assert client_user.verify_password(data["new_password"])


def test_fetch_my_user_profile(test_client, client_user):
    """
    GIVEN a Flask application configured for testing and a user
    WHEN the 'user_profile_api' is requested (GET)
    THEN check the response is valid and fetch the user profile
    """

    response = test_client.get(
        url_for("user_profile_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched." in response.get_data()
    assert client_user.email == response.get_json()["data"]["email"]


def test_update_my_user_profile(test_client, client_user):
    """
    GIVEN a Flask application configured for testing and a user
    WHEN the 'user_profile_api' is posted to update my user profile (POST)
    THEN check the response is valid
    """

    phone_number = client_user.phone_number
    new_name = generate_username()

    data = {
        "username": new_name,
        "email": new_name + "@jmail.com",
        "phone_number": "071" + generate_number(7)
    }

    response = test_client.put(
        url_for("user_profile_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert "Your user profile has been updated" in response.get_json()["message"]
    assert client_user.email == new_name + "@jmail.com"
    assert client_user.username == new_name
    assert client_user.phone_number != phone_number


def test_admin_fetch_user_list(test_client, superadmin):
    """
    GIVEN a Flask application configured for testing and admin user
    WHEN the 'user_list_api' is requested (GET) by admin user
    THEN check the response is valid and fetch user lists
    """

    response = test_client.get(
        url_for("user_list_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()


def test_admin_fetch_user_details(test_client, superadmin, client_user):
    """
    GIVEN a Flask application configured for testing and admin user
    WHEN the 'user_detail_api' is requested (GET) by admin user
    THEN check the response is valid and fetch user detail
    """

    response = test_client.get(
        url_for("user_detail_api", user_id=client_user.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()
    assert client_user.email == response.get_json()["data"]["email"]

    """
    GIVEN a Flask application configured for testing and user
    WHEN the 'user_detail_api' is requested (GET) by a non-admin user
    THEN check the response is valid
    """

    response = test_client.get(
        url_for("user_detail_api", user_id=superadmin.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
    )

    assert response.status_code == 403
    assert response.get_json().get("status") == 403
    assert b"You don't have the permission" in response.get_data()
    assert "data" not in response.get_json()
