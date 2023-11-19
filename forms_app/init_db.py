import logging

from pymongo import ASCENDING, IndexModel, MongoClient

from forms_app.constants import DATA, EMAIL, PHONE, TEXT
from forms_app.settings import app_settings

mongodb_client: MongoClient = MongoClient(
    app_settings.mongo_host,
    app_settings.mongo_port,
)

logger = logging.getLogger(__name__)


def mongodb_init(client, settings):
    db = client[settings.db_name]
    collection = db[settings.form_collection]
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
            },
            "patternProperties": {
                "^(?!(_id|name)$).*": {"enum": [EMAIL, PHONE, DATA, TEXT]},
            },
        }
    }
    if settings.form_collection not in db.list_collection_names():
        db.create_collection(settings.form_collection)
    # Создание валидации для коллекции
    db.command(
        {
            "collMod": settings.form_collection,
            "validator": validator,
            "validationLevel": "moderate",
            "validationAction": "error",
        }
    )
    index = IndexModel([("name", ASCENDING)], name="name", unique=True)
    collection.create_indexes([index])
    logging.info(f"{collection} init")
    return client[settings.db_name]
