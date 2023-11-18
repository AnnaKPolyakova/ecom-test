import datetime as dt
import json
import logging
from os import makedirs

from flask import request


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if request:
            record.request_id = request.headers.get("X-Request-Id", "")
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": str(dt.datetime.fromtimestamp(record.created)),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "request_id": getattr(record, "request_id", "")
        }
        return json.dumps(log)


def get_logs_settings_dict(settings):
    log_dir = settings.log_dir
    log_file = log_dir + settings.log_file
    makedirs(log_dir, exist_ok=True)
    log_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    '()': 'forms_app.logs_init.JsonFormatter',
                },
                "simple": {
                    "format": "%(asctime)s - %(message)s",
                },
            },
            'filters': {
                'app_filter': {
                    '()': RequestIdFilter,
                },
            },
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': log_file,
                    'level': settings.log_level,
                    'formatter': 'standard',
                    'filters': ['app_filter'],
                },
                'console':
                    {
                        "class": "logging.StreamHandler",
                        'level': settings.log_level,
                        'formatter': 'simple',
                    }
            },
            'root': {
                'handlers': ['file', 'console'],
            },
            'loggers': {
                '': {
                    'handlers': ['file'],
                    'level': settings.log_level,
                    'propagate': True,
                },
            },
        }
    return log_dict
