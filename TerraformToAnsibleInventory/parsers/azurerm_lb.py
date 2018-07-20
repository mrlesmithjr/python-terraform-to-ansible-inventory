def parse(RESOURCE, TERRAFORM_LOAD_BALANCERS, TERRAFORM_PUBLIC_IPS):
    """Populate Azure LB info."""
    raw_attrs = RESOURCE['primary']['attributes']
    load_balancer = dict()
    public_ip_address = ''
    for pub_ip in TERRAFORM_PUBLIC_IPS:
        public_ip_address_id = (
            raw_attrs['frontend_ip_configuration.0.public_ip_address_id'])
        if pub_ip['id'] == public_ip_address_id:
            public_ip_address = pub_ip['ip_address']
    load_balancer.update({'location': raw_attrs['location'],
                          'name': raw_attrs['name'],
                          'public_ip_address': public_ip_address,
                          'sku': raw_attrs['sku'],
                          'type': 'azurerm_lb'})
    TERRAFORM_LOAD_BALANCERS.append(load_balancer)
