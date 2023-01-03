import pytest
import uuid

from flask import url_for
from flask_restful import Api

from api.utils import create_app, db, jwt
from api.urls import api_urls
from api.models import Role, User, TokenBlocklist
from tests.utils import create_user
from api.utils.application_data import roles


@pytest.fixture(scope="session")
def test_app():
    """Testing application"""

    # create and configure the app
    app = create_app('config.testing.TestingConfig', name="Testing")

    # Register Urls
    api = Api(app)
    api_urls(api)

    # jwt
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(uuid=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    return app


@pytest.fixture(scope='session')
def test_db(request, test_app):
    # setup
    print("\nPushing test application context")
    app_context = test_app.app_context()
    app_context.push()

    print("\nCreating test database tables", "\nDB:", db, "\n")
    db.drop_all()
    db.create_all()

    yield db

    # teardown
    db.session.remove()
    db.drop_all()

    print("\nPopping test application context\n")
    app_context.pop()


@pytest.fixture(scope="session")
def test_client(test_db, test_app):
    """Test client"""

    print("\nCreating test client")
    return test_app.test_client()


@pytest.fixture(scope="session")
def seed_db(test_db):
    """Seeds the database with initial data"""

    for role in roles:
        _role = Role.query.filter_by(name=role).one_or_none()
        print(f"Seeding Data: adding {role} role...")
        if not _role:
            role = Role(name=role, uuid=uuid.uuid1())
            db.session.add(role)
            db.session.commit()

    return


@pytest.fixture(scope="session")
def superadmin_role(seed_db):
    """Test SuperAdmin role"""

    return Role.query.filter_by(name="SuperAdmin").one_or_none()


@pytest.fixture(scope="session")
def admin_role(seed_db):
    """Test Admin role"""

    return Role.query.filter_by(name="Admin").one_or_none()


@pytest.fixture(scope="session")
def client_role(seed_db):
    """Test Client role"""

    return Role.query.filter_by(name="Client").one_or_none()


@pytest.fixture(scope="session")
def superadmin(test_db, test_client, superadmin_role):
    """Test SuperAdmin"""

    superadmin = create_user(superadmin_role, username="superadmin")

    superadmin.is_email_confirmed = True
    superadmin.set_auth_token(str(superadmin.uuid))

    test_db.session.add(superadmin)
    test_db.session.commit()

    superadmin = User.query.filter_by(username="superadmin").one_or_none()

    return superadmin


@pytest.fixture(scope="module")
def client_user(test_db, test_client, client_role):
    """Test Client"""

    user = create_user(client_role)

    username = user.username

    test_db.session.add(user)
    test_db.session.commit()

    user = User.query.filter_by(username=username).one_or_none()

    test_client.get(url_for("user_confirm-email_api", token=user.email_confirm_token))

    user.set_auth_token(user.uuid)

    return user
