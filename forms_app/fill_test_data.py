import random

from forms_app.settings import app_settings
from forms_app.init_db import mongodb_client


def fill_data():
    db = mongodb_client[app_settings.db_name]
    collection = db[app_settings.form_collection]
    documents = [
        {
            "name": "base",
            "email": "email",
            "phone": "phone",
            "data": "data",
            "text": "text",
        }
    ]
    fields = ["email", "phone", "data", "text"]
    for i in range(app_settings.number_of_test_data):
        n = random.randint(1, 10)
        new_obj = {"name": "base" + str(i)}
        for _ in range(n):
            new_obj["field_" + str(random.randint(1, 10))] = random.choice(
                fields)
        documents.append(new_obj)
    collection.insert_many(documents)


if __name__ == "__main__":
    fill_data()
