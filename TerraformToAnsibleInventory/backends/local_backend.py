import json
from .. logging_config import setup as LoggingConfigSetup


def load(LOG_LEVEL, TERRAFORM_TFSTATE):
    """Collect local backend data."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    with open(TERRAFORM_TFSTATE) as json_file:
        LOGGER.info('Loading %s' % TERRAFORM_TFSTATE)
        DATA = json.load(json_file)
        LOGGER.debug(DATA)

    return DATA
