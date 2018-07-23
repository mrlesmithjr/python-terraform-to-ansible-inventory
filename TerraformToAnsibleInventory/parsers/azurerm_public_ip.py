from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_PUBLIC_IPS):
    """Populate Azure public IP info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    public_ip = dict()
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    public_ip.update({'id': raw_attrs['id'],
                      'ip_address': raw_attrs['ip_address']})
    TERRAFORM_PUBLIC_IPS.append(public_ip)
