import pytest

from api.utils import create_app, db


@pytest.fixture(scope="session")
def test_client():
    """Testing application"""

    # create and configure the app
    app = create_app('config/testing.py', name="Testing")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='session')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    yield  # this is where the testing happens!

    db.drop_all()
