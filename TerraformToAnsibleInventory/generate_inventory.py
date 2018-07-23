import yaml
import json
from . logging_config import setup as LoggingConfigSetup


def ansible(LOG_LEVEL, TERRAFORM_ANSIBLE_GROUPS,
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

    TERRAFORM_VMS['terraform_load_balancers'] = dict()
    TERRAFORM_VMS['terraform_load_balancers']['hosts'] = dict()
    if TERRAFORM_LOAD_BALANCERS != []:
        for lb in TERRAFORM_LOAD_BALANCERS:
            TERRAFORM_VMS['terraform_load_balancers']['hosts'].update(
                {lb['name']: lb})
            if lb['type'] not in TERRAFORM_VMS:
                TERRAFORM_VMS[lb['type']] = dict()
                TERRAFORM_VMS[lb['type']]['hosts'] = dict()
                TERRAFORM_VMS[lb['type']]['hosts'][lb['name']] = dict()

    generate(TERRAFORM_VMS, TERRAFORM_ANSIBLE_INVENTORY, LOG_LEVEL)


def generate(TERRAFORM_VMS, TERRAFORM_ANSIBLE_INVENTORY, LOG_LEVEL):
    """Finally generate a functional Ansible inventory file."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    TERRAFORM_VMS = yaml.load(json.dumps(TERRAFORM_VMS))

    with open(TERRAFORM_ANSIBLE_INVENTORY, 'w') as yaml_file:
        LOGGER.info('Inventory saved to: %s' % TERRAFORM_ANSIBLE_INVENTORY)
        yaml.dump(TERRAFORM_VMS, yaml_file, default_flow_style=False)
