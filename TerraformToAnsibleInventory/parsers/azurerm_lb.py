from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_LOAD_BALANCERS, TERRAFORM_PUBLIC_IPS):
    """Populate Azure LB info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    load_balancer = dict()
    public_ip_address = ''

    for pub_ip in TERRAFORM_PUBLIC_IPS:
        public_ip_address_id = (
            raw_attrs['frontend_ip_configuration.0.public_ip_address_id'])
        if pub_ip['id'] == public_ip_address_id:
            public_ip_address = pub_ip['ip_address']

    load_balancer.update(
        {
            'location': raw_attrs['location'],
            'name': raw_attrs['name'],
            'private_ip_address':
            raw_attrs['private_ip_address'],
            'public_ip_address': public_ip_address,
            'resource_group_name':
            raw_attrs['resource_group_name'],
            'sku': raw_attrs['sku'],
            'type': 'azurerm_lb'
        }
    )

    TERRAFORM_LOAD_BALANCERS.append(load_balancer)
