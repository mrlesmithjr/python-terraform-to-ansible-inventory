import ast


def parse(RESOURCE, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS):
    """Populate Azure VM info."""
    vm = dict()
    raw_attrs = RESOURCE['primary']['attributes']
    try:
        ansible_groups = []
        groups = ast.literal_eval(raw_attrs['tags.ansible_groups'])
        for group in groups:
            ansible_groups.append(group)
            if group not in TERRAFORM_ANSIBLE_GROUPS:
                TERRAFORM_ANSIBLE_GROUPS.append(group)
    except KeyError:
        ansible_groups = []

    vm.update(
        {'data_type': RESOURCE['type'], 'inventory_hostname': raw_attrs['name'],
         'id': raw_attrs['id'], 'location': raw_attrs['location'],
         'resource_group_name': raw_attrs['resource_group_name'],
         'target': RESOURCE['type'] + "." + raw_attrs['name'],
         'vm_size': raw_attrs['vm_size'],
         'ansible_groups': ansible_groups})
    TERRAFORM_VMS.append(vm)
