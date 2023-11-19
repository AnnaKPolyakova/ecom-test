from logging.config import dictConfig

from flask import Flask

from forms_app.api.v1.endpoints import form_api
from forms_app.init_db import mongodb_client, mongodb_init
from forms_app.logs_init import get_logs_settings_dict
from forms_app.settings import app_settings
from forms_app.utils import form_app_doc


def create_forms_app(settings):
    dictConfig(get_logs_settings_dict(settings))
    current_app = Flask(__name__)
    current_app.register_blueprint(form_api, url_prefix="/api/v1")
    form_app_doc.register(current_app)
    mongodb_init(mongodb_client, settings)
    return current_app


if __name__ == "__main__":
    app = create_forms_app(app_settings)
    app.run(port=5000)
