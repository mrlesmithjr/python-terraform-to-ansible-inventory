from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, NAME, TERRAFORM_VMS):
    """Populate AWS VM info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    VM = dict()
    ansible_groups = []
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    VM_NAME = raw_attrs['id']
    VPC_SECURITY_GROUP_IDS = []

    for KEY, VALUE in raw_attrs.items():
        if 'vpc_security_group_ids' in KEY and '#' not in KEY:
            VPC_SECURITY_GROUP_IDS.append(VALUE)

    VM.update(
        {
            'ansible_host': raw_attrs['private_ip'],
            'data_type': RESOURCE['type'], 'inventory_hostname': VM_NAME,
            'ami': raw_attrs['ami'],
            'ansible_groups': ansible_groups,
            'availability_zone': raw_attrs['availability_zone'],
            'instance_type': raw_attrs['instance_type'],
            'key_name': raw_attrs['key_name'],
            'network_interface_id': raw_attrs['network_interface_id'],
            'private_dns': raw_attrs['private_dns'],
            'private_ip': raw_attrs['private_ip'],
            'public_dns': raw_attrs['public_dns'],
            'public_ip': raw_attrs['public_ip'],
            'subnet_id': raw_attrs['subnet_id'],
            'target': NAME,
            'vpc_security_group_ids': VPC_SECURITY_GROUP_IDS
        }
    )

    TERRAFORM_VMS.append(VM)
