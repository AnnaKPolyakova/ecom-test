
from logging.config import dictConfig

from flask import Flask, request

from forms_app.api.v1.endpoints import form_api
# from flask_jwt_extended import JWTManager

# from forms_app.api.v1.bookmark import bookmark_api
# from forms_app.api.v1.movie_rating import movie_rating_api
# from forms_app.api.v1.review import review_api
# from forms_app.api.v1.review_rating import review_rating_api
from forms_app.init_db import mongodb_client, mongodb_init
from forms_app.settings import app_settings
from forms_app.utils import form_app_doc

from forms_app.logs_init import get_logs_settings_dict


def create_forms_app(settings):
    dictConfig(get_logs_settings_dict(settings))
    current_app = Flask(__name__)
    current_app.register_blueprint(
        form_api, url_prefix="/api/v1"
    )
    form_app_doc.register(current_app)
    # current_app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    # current_app.config["JWT_HEADER_NAME"] = "Authorization"
    # current_app.config["JWT_HEADER_TYPE"] = "Bearer"
    # current_app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    # JWTManager(current_app)
    mongodb_init(mongodb_client, settings)
    return current_app


if __name__ == "__main__":
    app = create_forms_app(app_settings)
    app.run(port=5000)
