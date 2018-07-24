from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_NETWORK_INTERFACES):
    """Populate Azure network interface info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    interface = dict()
    private_ips = []
    public_ips = []
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    num_ips = int(raw_attrs['ip_configuration.#'])
    for count in xrange(num_ips):
        private_ips.append(
            raw_attrs['private_ip_addresses.%s' % count])
        public_ips.append(
            raw_attrs['ip_configuration.%s.public_ip_address_id' % count])

    interface.update(
        {
            'virtual_machine_id': raw_attrs['virtual_machine_id'],
            'mac_address': raw_attrs['mac_address'],
            'private_ip_address': raw_attrs['private_ip_address'],
            'private_ips': private_ips,
            'public_ips': public_ips
        }
    )

    try:
        raw_attrs['network_security_group_id']
        interface.update(
            {
                'network_security_group_id':
                raw_attrs['network_security_group_id']
            }
        )
    except KeyError:
        LOGGER.debug(KeyError)
        pass

    TERRAFORM_NETWORK_INTERFACES.append(interface)
