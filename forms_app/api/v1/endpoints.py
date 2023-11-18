import logging
from http import HTTPStatus

from flask import Blueprint, request
from spectree import Response

from forms_app.api.v1.models import Name, FormDescription, Status, Data
from forms_app.api.v1.servises import FormFinder, CHECKS_AND_TYPES
from forms_app.constants import TYPE_INVALID
from forms_app.utils import form_app_doc

form_api = Blueprint("form", __name__)


@form_api.route("/get_form/", methods=["POST"])
@form_app_doc.validate(
    tags=["form"],
    json=Data,
    resp=Response(
        HTTP_200=(Name, "Ok"),
        HTTP_404=(FormDescription, "Not found"),
        HTTP_400=(Status, "Error"),
    ),
)
def get_form():
    logging.debug("get_form api start")
    if request.content_type != 'application/json':
        logging.error("get_form api: {error}".format(error="json_invalid"))
        return {"status": False, "info": {"body": "json_invalid"}}, \
            HTTPStatus.BAD_REQUEST
    try:
        res, status = FormFinder(
            request.get_json(), CHECKS_AND_TYPES
        ).get_form_name()
    except Exception as error:
        logging.error("get_form api: {error}".format(error=error))
        return {"status": False}, HTTPStatus.BAD_REQUEST
    if status is False:
        if TYPE_INVALID in res.values():
            return {"status": False, "info": res}, HTTPStatus.BAD_REQUEST
        return res, HTTPStatus.NOT_FOUND
    logging.debug("get_form api end")
    return res, HTTPStatus.OK
