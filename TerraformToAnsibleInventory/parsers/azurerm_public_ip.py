from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_PUBLIC_IPS):
    """Populate Azure public IP info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    PUBLIC_IP = dict()
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)

    PUBLIC_IP.update(
        {
            'id': raw_attrs['id'],
            'ip_address': raw_attrs['ip_address']
        }
    )

    TERRAFORM_PUBLIC_IPS.append(PUBLIC_IP)
