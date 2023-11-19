import json
import random
from http import HTTPStatus

import pytest
from conftest import (DATA_TEST_DD_MM_YYYY, DATA_TEST_YYYY_MM_DD, EMAIL_TEST,
                      PHONE_TEST_NOT_RU, PHONE_TEST_RU, TEXT_TEST)
from flask import url_for

from forms_app.constants import DATA, EMAIL, PHONE, TEXT, TYPE_INVALID


class TestFormAPI:
    def test_form_with_empty_json(self, test_client, forma_base, collection):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(url, json=dict())
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.OK
        name = collection.find({"_id": forma_base})[0]["name"]
        assert data == {"name": name}

    def test_form_without_json(self, test_client, forma_base):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url,
        )
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.BAD_REQUEST
        assert data == {"info": {"body": "json_invalid"}, "status": False}

    def test_form_without_wrong_fields_types(self, test_client, forma_base):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(url, json={"field": 1})
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.BAD_REQUEST
        assert data == {"info": {"field": TYPE_INVALID}, "status": False}

    def test_form_with_field_not_exist(self, test_client, forma_base):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        field = str((random.uniform(1.0, 10.0)))
        response = getattr(test_client, method)(url, json={field: "test"})
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.NOT_FOUND
        assert data == {field: TEXT.upper()}

    @pytest.mark.parametrize(
        "field, value, value_type",
        [
            ("email", TEXT_TEST, TEXT),
            ("email", DATA_TEST_DD_MM_YYYY, DATA),
            ("email", DATA_TEST_YYYY_MM_DD, DATA),
            ("email", PHONE_TEST_RU, PHONE),
            ("phone", TEXT_TEST, TEXT),
            ("phone", DATA_TEST_DD_MM_YYYY, DATA),
            ("phone", DATA_TEST_YYYY_MM_DD, DATA),
            ("phone", EMAIL_TEST, EMAIL),
            ("phone", PHONE_TEST_NOT_RU, TEXT),
            ("data", TEXT_TEST, TEXT),
            ("data", EMAIL_TEST, EMAIL),
            ("data", PHONE_TEST_RU, PHONE),
            ("text", EMAIL_TEST, EMAIL),
            ("text", PHONE_TEST_RU, PHONE),
            ("text", DATA_TEST_DD_MM_YYYY, DATA),
        ],
    )
    def test_form_with_field_exist_but_with_other_type(
        self, test_client, forma_base, value, field, value_type
    ):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(url, json={field: value})
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.NOT_FOUND
        assert data == {field: value_type.upper()}

    def test_form_with_field_exist_data_format_dd_mm_yyyy(
        self, test_client, collection, forma_base
    ):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url,
            json={
                "email": EMAIL_TEST,
                "phone": PHONE_TEST_RU,
                "data": DATA_TEST_DD_MM_YYYY,
                "text": TEXT_TEST,
            },
        )
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.OK
        name = collection.find({"_id": forma_base})[0]["name"]
        assert data == {"name": name}

    def test_form_with_field_exist_data_format_yyyy_mm_dd(
        self, test_client, collection, forma_base
    ):
        url = url_for("form.get_form")
        method = "post"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url,
            json={
                "email": EMAIL_TEST,
                "phone": PHONE_TEST_RU,
                "data": DATA_TEST_YYYY_MM_DD,
                "text": TEXT_TEST,
            },
        )
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.OK
        name = collection.find({"_id": forma_base})[0]["name"]
        assert data == {"name": name}
