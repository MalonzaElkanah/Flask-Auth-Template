import pytest

from api.utils import create_app


@pytest.fixture(scope="session")
def test_app():
    """Testing application"""

    # create and configure the app
    app = create_app('config/testing.py', name="Testing")

    return app
