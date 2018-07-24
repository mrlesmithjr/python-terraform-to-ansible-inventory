from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_VMS):
    """Populate vSphere VM info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    VM = dict()
    ANSIBLE_GROUPS = []
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)

    VM.update(
        {
            'ansible_host': raw_attrs['network_interface.0.ipv4_address'],
            'data_type': RESOURCE['type'], 'id': raw_attrs['id'],
            'mac_address': raw_attrs['network_interface.0.mac_address'],
            'memory': raw_attrs['memory'],
            'inventory_hostname': raw_attrs['name'],
            'network_label': raw_attrs['network_interface.0.label'],
            'target': RESOURCE['type'] + "." + raw_attrs['name'],
            'uuid': raw_attrs['uuid'], 'vcpu': raw_attrs['vcpu'],
            'ansible_groups': ANSIBLE_GROUPS
        }
    )

    TERRAFORM_VMS.append(VM)
