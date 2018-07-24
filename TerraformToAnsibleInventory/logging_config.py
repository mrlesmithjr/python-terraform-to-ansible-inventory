import logging
import logging.config
import json

ATTR_TO_JSON = [
    'created', 'filename', 'funcName', 'levelname', 'lineno',
    'module', 'msecs', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'thread', 'threadName'
]


class JsonFormatter:
    def format(self, record):
        obj = {attr: getattr(record, attr)
               for attr in ATTR_TO_JSON}
        return json.dumps(obj, indent=4)


def setup(LOG_LEVEL):
    """Sets up and configures logging functionality."""
    LOG_LEVELS = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    HANDLER = logging.StreamHandler()
    HANDLER.formatter = JsonFormatter()
    logging.basicConfig(level=LOG_LEVELS[LOG_LEVEL])
    LOGGER = logging.getLogger(__name__)
    LOGGER.addHandler(HANDLER)

    return LOGGER
