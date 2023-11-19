import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic.v1 import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    log_file: str = Field(
        json_schema_extra={"env": "LOG_FILE"}, default="app.json"
    )
    log_dir: str = Field(
        json_schema_extra={"env": "LOG_DIR"}, default="../logs/"
    )
    log_level: str = Field(
        json_schema_extra={"env": "LOG_LEVEL"}, default="INFO"
    )
    db_name: str = Field(
        json_schema_extra={"env": "DB_NAME"}, default="form_db"
    )
    test_db_name: str = Field(
        json_schema_extra={"env": "TEST_DB_NAME"}, default="form_db"
    )
    form_collection: str = Field(
        json_schema_extra={"env": "FORM_COLLECTION"}, default="form"
    )
    mongo_host: str = Field(
        json_schema_extra={"env": "MONGO_HOST"}, default="localhost"
    )
    mongo_port: int = Field(
        json_schema_extra={"env": "MONGO_PORT"}, default=27017
    )
    number_of_test_data: int = Field(
        json_schema_extra={"env": "NUMBER_OF_TEST_DATA"}, default=100
    )

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


app_settings = Settings()
