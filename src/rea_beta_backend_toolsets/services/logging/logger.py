from __future__ import annotations

import atexit
import datetime as dt
import json
import logging.handlers
import pathlib
import queue
from logging.handlers import QueueHandler
from logging.handlers import QueueListener

from typing_extensions import override

from .constants import LOG_RECORD_BUILTIN_ATTRS
from .constants import LOGGING_CONFIG_FILE_PATH


class ReaJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            'message': record.getMessage(),
            'timestamp': dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc,
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields['exc_info'] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields['stack_info'] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= logging.INFO


def setup_logging():
    config_file = pathlib.Path(LOGGING_CONFIG_FILE_PATH)
    with open(config_file) as f_in:
        config = json.load(f_in)

    try:
        logging.config.dictConfig(config)
    except Exception as e:
        print(f'Error configuring logging: {e}')
        return

    log_queue = queue.Queue(-1)  # Create an actual Queue instance
    queue_handler = QueueHandler(log_queue)

    handlers = {
        handler.name: handler for handler in logging.getLogger().handlers
    }

    stderr_handler = handlers.get('stderr')
    file_json_handler = handlers.get('file_json')

    listener = QueueListener(log_queue, stderr_handler, file_json_handler)
    logging.getLogger().addHandler(queue_handler)
    listener.start()
    atexit.register(listener.stop)
