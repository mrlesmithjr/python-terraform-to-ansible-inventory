import ast
from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, NAME, RESOURCE, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS):
    """Populate Azure VM info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    vm = dict()
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)

    try:
        ansible_groups = []
        groups = ast.literal_eval(raw_attrs['tags.ansible_groups'])
        for group in groups:
            ansible_groups.append(group)
            if group not in TERRAFORM_ANSIBLE_GROUPS:
                TERRAFORM_ANSIBLE_GROUPS.append(group)
    except KeyError:
        LOGGER.debug(KeyError)
        ansible_groups = []

    vm.update(
        {
            'data_type': RESOURCE['type'],
            'inventory_hostname': raw_attrs['name'],
            'id': raw_attrs['id'],
            'location': raw_attrs['location'],
            'resource_group_name': raw_attrs['resource_group_name'],
            'target': NAME,
            'vm_size': raw_attrs['vm_size'],
            'ansible_groups': ansible_groups
        }
    )

    TERRAFORM_VMS.append(vm)
