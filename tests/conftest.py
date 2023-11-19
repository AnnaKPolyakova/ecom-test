import logging

import pytest

from forms_app.settings import app_settings

ERROR_INFO = "Check that {method} request {url} returns status {status}"

DATA_TEST_DD_MM_YYYY = "12.02.2012"
DATA_TEST_YYYY_MM_DD = "2012.02.12"
PHONE_TEST_RU = "+79151120202"
PHONE_TEST_NOT_RU = "+49151120202"
TEXT_TEST = "Test"
EMAIL_TEST = "Test@test.ru"


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

    app_settings.db_name = app_settings.test_db_name
    app = create_forms_app(app_settings)
    app.config["SERVER_NAME"] = "localhost"
    app.config["TESTING"] = True
    yield app


@pytest.fixture(scope="session")
def test_client(test_db, test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


@pytest.fixture(scope="session")
def collection(test_db, test_app):
    return test_db[app_settings.form_collection]


@pytest.fixture(scope="session")
def forma_base(test_db, test_app, collection):
    data = {
        "name": "base",
        "email": "email",
        "phone": "phone",
        "data": "data",
        "text": "text",
    }
    result = collection.insert_one(data)
    yield result.inserted_id
    collection.delete_one({"_id": result.inserted_id})
