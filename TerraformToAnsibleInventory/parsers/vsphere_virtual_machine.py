def parse(RESOURCE, TERRAFORM_VMS):
    """Populate vSphere VM info."""
    vm = dict()
    ansible_groups = []
    raw_attrs = RESOURCE['primary']['attributes']
    vm.update(
        {'ansible_host': raw_attrs['network_interface.0.ipv4_address'],
         'data_type': RESOURCE['type'], 'id': raw_attrs['id'],
         'mac_address': raw_attrs['network_interface.0.mac_address'],
         'memory': raw_attrs['memory'],
         'inventory_hostname': raw_attrs['name'],
         'network_label': raw_attrs['network_interface.0.label'],
         'target': RESOURCE['type'] + "." + raw_attrs['name'],
         'uuid': raw_attrs['uuid'], 'vcpu': raw_attrs['vcpu'],
         'ansible_groups': ansible_groups})
    TERRAFORM_VMS.append(vm)
