from datetime import datetime

import phonenumbers
from validate_email_address import validate_email

from forms_app.constants import DATA, EMAIL, PHONE, TEXT, TYPE_INVALID
from forms_app.init_db import mongodb_client
from forms_app.settings import app_settings


def is_date_type(value: str):
    for format_data in ["%d.%m.%Y", "%Y.%m.%d"]:
        try:
            datetime.strptime(value, format_data)
            return True
        except ValueError:
            pass
    return False


def is_phone_type(value: str):
    try:
        parsed_number = phonenumbers.parse(value)
        if phonenumbers.region_code_for_number(parsed_number) == "RU":
            return True
        return False
    except phonenumbers.NumberParseException:
        return False


def is_email_type(value: str):
    if validate_email(value):
        return True
    else:
        return False


CHECKS_AND_TYPES = {
    is_date_type: DATA,
    is_phone_type: PHONE,
    is_email_type: EMAIL,
}


class FormFinder:
    def __init__(self, dict_obj: dict, checks_and_types: dict):
        self.validate: bool = True
        self.dict_obj: dict = dict_obj
        self.checks_and_types: dict = checks_and_types
        self.query_criteria: dict = dict()
        self.forms: list = []
        self.fields_info: dict = dict()

    def _get_query_criteria(self):
        for field, value in self.dict_obj.items():
            type_name = self._get_field_type(value)
            if type_name:
                self.query_criteria[field] = type_name
            else:
                self.query_criteria[field] = TYPE_INVALID
                self.validate = False

    def _get_forms(self):
        db = mongodb_client[app_settings.db_name]
        collection = db[app_settings.form_collection]
        result = collection.find(self.query_criteria)
        self.forms = list(sorted(result, key=lambda x: len(x)))

    def _get_field_type(self, value):
        if not isinstance(value, str):
            self.validate = False
            return TYPE_INVALID
        for func, type_name in self.checks_and_types.items():
            if func(value) is True:
                return type_name
        return TEXT

    def get_form_name(self):
        self._get_query_criteria()
        if self.validate is False:
            return self.query_criteria, False
        self._get_forms()
        if len(self.forms) == 0:
            if self.validate:
                for field, type_name in self.query_criteria.items():
                    self.query_criteria[field] = type_name.upper()
            return self.query_criteria, False
        return {"name": self.forms[0].get("name", "")}, True
