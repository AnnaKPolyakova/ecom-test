from typing import Dict, Optional

from pydantic.v1 import BaseModel, Extra


class Name(BaseModel):
    name: str


class Status(BaseModel):
    status: bool
    info: Optional[dict]


class FormDescription(BaseModel):
    class Config:
        extra = Extra.allow

    examples = {
        "data": {
            "field1": "email",
            "field2": "phone",
            "field3": "data",
            "field4": "text",
        }
    }


class Data(BaseModel):
    class Config:
        extra = Extra.allow

    examples = {
        "field1": "test@test.ru",
        "field2": "+79000000000",
        "field3": "12.02.2013",
        "field4": "text",
    }

