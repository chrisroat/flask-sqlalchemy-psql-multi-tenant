import os

import pytest
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from app import ProdConfig, create_app, db


class TestConfig(ProdConfig):
    DEBUG = True
    TESTING = True


@pytest.fixture
def test_db_uri(request: type[pytest.FixtureRequest]):
    """Creates a database for testing with a random name."""
    base_uri = os.environ["TEST_DB_HOST"]  # postgresql://[USER[:PASSWORD]]@HOST
    db_uri = f"{base_uri}/{os.urandom(12).hex()}"
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)

    @request.addfinalizer
    def cleanup():
        drop_database(db_uri)

    return db_uri


@pytest.fixture
def app(test_db_uri: str):
    """Configure Flask app for testing."""

    # Update default and bound database URIs
    TestConfig.SQLALCHEMY_DATABASE_URI = test_db_uri
    for k in TestConfig.SQLALCHEMY_BINDS:
        TestConfig.SQLALCHEMY_BINDS[k] = test_db_uri

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all(bind_key="global")

    return app
