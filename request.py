import random

import requests

URL = "http://127.0.0.1:5000/api/v1/get_form/"


def form_with_empty_json():
    print(form_with_empty_json.__name__)
    json_data = dict()
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_without_json():
    print(form_with_empty_json.__name__)
    json_data = "without json"
    response = requests.post(URL)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_without_wrong_fields_types():
    print(form_without_wrong_fields_types.__name__)
    json_data = {"field": 1}
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_with_field_not_exist():
    print(form_with_field_not_exist.__name__)
    json_data = {str((random.uniform(1.0, 10.0))): "test"}
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_with_field_exist_but_with_other_type():
    print(form_with_field_exist_but_with_other_type.__name__)
    json_data = {"phone": "example"}
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_with_field_exist_data_format_dd_mm_yyyy():
    print(form_with_field_exist_data_format_dd_mm_yyyy.__name__)
    json_data = {
        "email": "example@example.ru",
        "phone": "+79151066071",
        "data": "12.02.2012",
        "text": "example",
    }
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


def form_with_field_exist_data_format_yyyy_mm_dd():
    print(form_with_field_exist_data_format_yyyy_mm_dd.__name__)
    json_data = {
        "email": "example@example.ru",
        "phone": "+79151066071",
        "data": "2012.12.02",
        "text": "example",
    }
    response = requests.post(URL, json=json_data)
    print("json: {data}".format(data=json_data))
    print("data: {data}".format(data=response.json()))
    print(
        "status_code: {status_code}".format(status_code=response.status_code)
    )
    print()


if __name__ == "__main__":
    form_with_empty_json()
    form_without_json()
    form_without_wrong_fields_types()
    form_with_field_not_exist()
    form_with_field_exist_but_with_other_type()
    form_with_field_exist_data_format_dd_mm_yyyy()
    form_with_field_exist_data_format_yyyy_mm_dd()
