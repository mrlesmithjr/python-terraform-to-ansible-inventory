from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, NAME, TERRAFORM_VMS):
    """Populate AWS VM info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    vm = dict()
    ansible_groups = []
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    vm_name = NAME.split('.')[1]
    vm.update({'ansible_host': raw_attrs['private_ip'],
               'data_type': RESOURCE['type'], 'inventory_hostname': vm_name,
               'ami': raw_attrs['ami'],
               'ansible_groups': ansible_groups,
               'availability_zone': raw_attrs['availability_zone'],
               'instance_type': raw_attrs['instance_type'],
               'private_ip': raw_attrs['private_ip'],
               'public_ip': raw_attrs['public_ip']})
    TERRAFORM_VMS.append(vm)
