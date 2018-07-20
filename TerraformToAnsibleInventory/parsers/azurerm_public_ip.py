def parse(RESOURCE, TERRAFORM_PUBLIC_IPS):
    """Populate Azure public IP info."""
    public_ip = dict()
    raw_attrs = RESOURCE['primary']['attributes']
    public_ip.update({'id': raw_attrs['id'],
                      'ip_address': raw_attrs['ip_address']})
    TERRAFORM_PUBLIC_IPS.append(public_ip)
