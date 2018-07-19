def parse(DATA, TERRAFORM_NETWORK_INTERFACES):
    """Populate Azure network interface info."""
    interface = dict()
    private_ips = []
    public_ips = []
    raw_attrs = DATA['primary']['attributes']
    num_ips = int(raw_attrs['ip_configuration.#'])
    for count in xrange(num_ips):
        private_ips.append(
            raw_attrs['private_ip_addresses.%s' % count])
        public_ips.append(
            raw_attrs['ip_configuration.%s.public_ip_address_id' % count])
    interface.update({'virtual_machine_id': raw_attrs['virtual_machine_id'],
                      'mac_address': raw_attrs['mac_address'],
                      'private_ip_address': raw_attrs['private_ip_address'],
                      'private_ips': private_ips,
                      'public_ips': public_ips})
    TERRAFORM_NETWORK_INTERFACES.append(interface)
