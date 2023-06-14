import logging

from flask import Blueprint, request

from .handlers import prepare_data, save_data
from .utils import convert_timestamp_to_epoch

routes = Blueprint('main', __name__)


@routes.post("/data")
def post_data():
    # TODO: parse incoming data, and save it to the database
    # data is of the form:
    #  {timestamp} {name} {value}

    try:
        save_data(request)
        return {"success": "true"}
    except Exception:
        logging.exception("Internal server error")
        return {"success": "false"}


@routes.get("/data")
def get_data():
    # TODO: check what dates have been requested, and retrieve all data within the given range
    date_from = request.args.get('from')
    date_to = request.args.get('to')

    try:
        start_key = convert_timestamp_to_epoch(date_from)
        end_key = convert_timestamp_to_epoch(date_to)
    except Exception:
        logging.exception("Internal server error")
        raise

    output = prepare_data(start_key, end_key)

    return output
