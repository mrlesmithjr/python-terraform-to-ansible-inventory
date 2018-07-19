import yaml
import json


def ansible(TERRAFORM_ANSIBLE_GROUPS,
            TERRAFORM_ANSIBLE_INVENTORY,
            TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
            TERRAFORM_LOAD_BALANCERS):
    """Generate Terraform inventory for Ansible and write to inventory file."""
    # Reset TERRAFORM_VMS for new collection
    TERRAFORM_VMS = dict()

    for group in TERRAFORM_ANSIBLE_GROUPS:
        TERRAFORM_VMS[group] = dict()
        TERRAFORM_VMS[group]['hosts'] = dict()

    for data_type in TERRAFORM_DATA_TYPES:
        TERRAFORM_VMS[data_type] = dict()
        TERRAFORM_VMS[data_type]['hosts'] = dict()

    TERRAFORM_VMS['terraform_vms'] = dict()
    TERRAFORM_VMS['terraform_vms']['hosts'] = dict()

    for vm in TERRAFORM_INVENTORY:
        TERRAFORM_VMS[vm['data_type']]['hosts'].update(
            {vm['inventory_hostname']: dict()})

        TERRAFORM_VMS['terraform_vms']['hosts'][vm['inventory_hostname']] = vm

        for group in vm['ansible_groups']:
            TERRAFORM_VMS[group]['hosts'][vm['inventory_hostname']] = dict()

    TERRAFORM_VMS['terraform_vms']['vars'] = dict()
    if TERRAFORM_LOAD_BALANCERS != []:
        TERRAFORM_VMS['terraform_vms']['vars'].update(
            {'terraform_load_balancers': TERRAFORM_LOAD_BALANCERS})

    TERRAFORM_VMS = yaml.load(json.dumps(TERRAFORM_VMS))

    with open(TERRAFORM_ANSIBLE_INVENTORY, 'w') as yaml_file:
        yaml.dump(TERRAFORM_VMS, yaml_file, default_flow_style=False)
