import logging

import pytest

from forms_app.settings import app_settings

ERROR_INFO = (
    "Check that {method} request {url} returns status {status}"
)


@pytest.fixture(scope="session", autouse=True)
def test_db():
    from forms_app.init_db import mongodb_client

    try:
        db = mongodb_client[app_settings.test_db_name]
    except Exception as error:
        logging.error(error)
    else:
        yield db
        mongodb_client.drop_database(app_settings.test_db_name)


@pytest.fixture(scope="session", autouse=True)
def test_app(test_db):
    from forms_app.app import create_forms_app
    app = create_forms_app(app_settings)
    app.config["SERVER_NAME"] = "localhost"
    app.config["TESTING"] = True
    yield app


@pytest.fixture(scope="session")
def test_client(test_db, test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client
