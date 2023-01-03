import json
import uuid

import pytest
from flask import url_for

from api.models import Role
from tests.utils import generate_username


@pytest.fixture(scope="module")
def test_role(test_db, test_client, client_role):
    """Test Role"""

    name = generate_username()

    role = Role(name=name, uuid=uuid.uuid1())

    test_db.session.add(role)
    test_db.session.commit()

    role = Role.query.filter_by(name=name).one_or_none()

    return role


def test_admin_fetch_role_list(test_client, superadmin, client_user):
    """
    GIVEN a Flask application configured for testing and admin user
    WHEN the 'user_roles_api' is requested (GET) by admin user
    THEN check the response is valid and fetch role list
    """

    response = test_client.get(
        url_for("user_roles_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()
    assert "data" in response.get_json()

    """
    GIVEN a Flask application configured for testing and user
    WHEN the 'user_roles_api' is requested (GET) by a non-admin user
    THEN check the response is valid
    """

    response = test_client.get(
        url_for("user_roles_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
    )

    assert response.status_code == 403
    assert response.get_json().get("status") == 403
    assert b"You don't have the permission" in response.get_data()
    assert "data" not in response.get_json()


def test_admin_add_role(test_client, superadmin):
    """
    GIVEN a Flask application configured for testing and admin user
    WHEN the 'user_roles_api' is posted (POST) by admin user to add new role
    THEN check the response is valid and role added
    """

    initial_role_count = Role.query.count()

    data = {
        "name": "tester"
    }

    response = test_client.post(
        url_for("user_roles_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 201
    assert response.get_json().get("status") == 201
    assert b"Role Created" in response.get_data()
    assert "data" in response.get_json()
    assert Role.query.count() == initial_role_count + 1


def test_admin_fetch_role_detail(test_client, superadmin, test_role):
    """
    GIVEN a Flask application configured for testing, test role and admin user
    WHEN the 'user_roles-detail_api' is requested (GET) by admin user to fetch role details
    THEN check the response is valid and fetch role details
    """

    response = test_client.get(
        url_for("user_roles-detail_api", role_id=test_role.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()
    assert test_role.name in response.get_json()["data"]["name"]


def test_admin_update_role(test_client, superadmin, test_role):
    """
    GIVEN a Flask application configured for testing, test role and admin user
    WHEN the 'user_roles-detail_api' is posted (PUT) by admin user to update role
    THEN check the response is valid and role updated
    """

    data = {
        "name": "new_role_name"
    }

    response = test_client.put(
        url_for("user_roles-detail_api", role_id=test_role.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert b"Role Updated" in response.get_data()
    assert "data" in response.get_json()
    assert data["name"] == test_role.name


def test_admin_delete_role(test_client, superadmin, test_role):
    """
    GIVEN a Flask application configured for testing, test role and admin user
    WHEN the 'user_roles-detail_api' is deleted (DELETE) by admin user to Delete a role
    THEN check the response is valid and role deleted
    """

    role_id = test_role.uuid

    response = test_client.delete(
        url_for("user_roles-detail_api", role_id=test_role.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Role Deleted" in response.get_data()
    assert Role.query.filter_by(uuid=role_id).one_or_none() is None
