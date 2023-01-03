import json
import uuid

import pytest
from flask import url_for

from api.models import Account
from tests.utils import generate_username


@pytest.fixture(scope="module")
def test_account(test_db, test_client, client_user):
    """Test Account"""

    account_uuid = str(uuid.uuid1())

    account = Account(
        user_id=client_user.uuid,
        name=generate_username(),
        bio_data=generate_username(),
        display_photo=generate_username(),
        uuid=account_uuid
    )

    test_db.session.add(account)
    test_db.session.commit()

    account = Account.query.filter_by(uuid=account_uuid).one_or_none()

    return account


def test_fetch_my_account_list(test_client, client_user):
    """
    GIVEN a Flask application configured for testing and user
    WHEN the 'user_accounts_api' is requested (GET) by user to fetch their accounts list
    THEN check the response is valid
    """

    response = test_client.get(
        url_for("user_accounts_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()
    assert "data" in response.get_json()


def test_add_account(test_client, client_user):
    """
    GIVEN a Flask application configured for testing and user
    WHEN the 'user_accounts_api' is posted (POST) by user to add new account
    THEN check the response is valid and account added
    """

    initial_acc_count = Account.query.filter_by(user_id=client_user.uuid).count()

    data = {
        "name": generate_username(),
        "bio_data": generate_username(),
        "display_photo": generate_username()
    }

    response = test_client.post(
        url_for("user_accounts_api"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {client_user.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 201
    assert response.get_json().get("status") == 201
    assert b"Account Created" in response.get_data()
    assert "data" in response.get_json()
    assert Account.query.filter_by(user_id=client_user.uuid).count() == initial_acc_count + 1


def test_fetch_account_detail(test_client, test_account, superadmin):
    """
    GIVEN a Flask application configured for testing, test account and user
    WHEN the 'user_accounts-detail_api' is requested (GET) by user to fetch their account details
    THEN check the response is valid and fetch account details
    """

    response = test_client.get(
        url_for("user_accounts-detail_api", account_id=test_account.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_account.user.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Data fetched" in response.get_data()
    assert test_account.name in response.get_json()["data"]["name"]

    """
    GIVEN a Flask application configured for testing, test account and user
    WHEN the 'user_accounts-detail_api' is requested (GET)
        by user to fetch account details not theirs
    THEN check the response is valid and not fetch account details
    """

    response = test_client.get(
        url_for("user_accounts-detail_api", account_id=test_account.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {superadmin.auth_token}",
        },
    )

    assert response.status_code == 404
    assert response.get_json().get("status") == 404
    assert b"Account not Found" in response.get_data()
    assert "data" not in response.get_json()


def test_update_account(test_client, test_account):
    """
    GIVEN a Flask application configured for testing and test account
    WHEN the 'user_accounts-detail_api' is posted (PUT) by account user to update
    THEN check the response is valid and account updated
    """

    data = {
        "name": generate_username(),
        "bio_data": generate_username(),
        "display_photo": generate_username()
    }

    response = test_client.put(
        url_for("user_accounts-detail_api", account_id=test_account.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_account.user.auth_token}",
        },
        data=json.dumps(data),
    )

    assert response.status_code == 200
    assert b"Account Updated" in response.get_data()
    assert "data" in response.get_json()
    assert data["name"] == test_account.name


def test_delete_account(test_client, test_account):
    """
    GIVEN a Flask application configured for testing, test account
    WHEN the 'user_accounts-detail_api' is deleted (DELETE) by account user
    THEN check the response is valid and account deleted
    """

    account_id = test_account.uuid

    response = test_client.delete(
        url_for("user_accounts-detail_api", account_id=test_account.uuid),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_account.user.auth_token}",
        },
    )

    assert response.status_code == 200
    assert b"Account Deleted" in response.get_data()
    assert Account.query.filter_by(uuid=account_id).one_or_none() is None
