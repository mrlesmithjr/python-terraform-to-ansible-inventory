from . logging_config import setup as LoggingConfigSetup


def terraform(LOG_LEVEL, TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
              TERRAFORM_NETWORK_INTERFACES,
              TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS,
              TERRAFORM_SECURITY_GROUPS):
    """Build Terraform inventory structure."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    for VM in TERRAFORM_VMS:
        if VM['data_type'] not in TERRAFORM_DATA_TYPES:
            TERRAFORM_DATA_TYPES.append(VM['data_type'])

        if VM['data_type'] == 'aws_instance':
            VM_INFO = aws_instance(LOGGER, VM, TERRAFORM_SECURITY_GROUPS)

        elif VM['data_type'] == 'azurerm_virtual_machine':
            VM_INFO = azurerm_virtual_machine(
                LOGGER, VM, TERRAFORM_NETWORK_INTERFACES, TERRAFORM_PUBLIC_IPS,
                TERRAFORM_SECURITY_GROUPS, TERRAFORM_INVENTORY)

        elif VM['data_type'] == 'vsphere_virtual_machine':
            VM_INFO = VM

        update_inventory(LOGGER, TERRAFORM_INVENTORY, VM_INFO)


def aws_instance(LOGGER, VM, TERRAFORM_SECURITY_GROUPS):
    """Generates Azure VM info to add to inventory."""
    VM_INFO = dict()
    LOGGER.info('Adding %s: %s to inventory.' %
                (VM['data_type'], VM['inventory_hostname']))

    VM_INFO.update(
        {
            'inventory_hostname': VM['inventory_hostname'],
            'ami': VM['ami'],
            'data_type': VM['data_type'],
            'ansible_groups': VM['ansible_groups'],
            'availability_zone': VM['availability_zone'],
            'instance_type': VM['instance_type'],
            'key_name': VM['key_name'],
            'network_interface_id': VM['network_interface_id'],
            'private_dns': VM['private_dns'],
            'private_ip': VM['private_ip'],
            'public_dns': VM['public_dns'],
            'public_ip': VM['public_ip'],
            'subnet_id': VM['subnet_id'],
            'target': VM['target'],
            'vpc_security_group_ids': VM['vpc_security_group_ids']
        }
    )

    for VPC_SECURITY_GROUP_ID in VM['vpc_security_group_ids']:
        for SECURITY_GROUP in TERRAFORM_SECURITY_GROUPS:
            if SECURITY_GROUP['id'] == VPC_SECURITY_GROUP_ID:
                VM_INFO.update(
                    {
                        'vpc_security_groups':
                        SECURITY_GROUP['security_groups']
                    }
                )

    return VM_INFO


def azurerm_virtual_machine(LOGGER, VM, TERRAFORM_NETWORK_INTERFACES,
                            TERRAFORM_PUBLIC_IPS, TERRAFORM_SECURITY_GROUPS,
                            TERRAFORM_INVENTORY):
    """Generates Azure VM info to add to inventory."""
    LOGGER.info('Adding %s: %s to inventory.' %
                (VM['data_type'], VM['inventory_hostname']))

    for interface in TERRAFORM_NETWORK_INTERFACES:
        if interface['virtual_machine_id'] == VM['id']:
            PUB_IPS = []
            VM_INFO = dict()
            LOGGER.debug(interface)
            for pub_ip in TERRAFORM_PUBLIC_IPS:
                if (pub_ip['id'] in interface['public_ips'] and
                        pub_ip['ip_address'] not in PUB_IPS):
                    PUB_IPS.append(pub_ip['ip_address'])

            VM_INFO.update(
                {
                    'inventory_hostname': VM['inventory_hostname'],
                    'data_type': VM['data_type'],
                    'ansible_host': interface['private_ip_address'],
                    'location': VM['location'],
                    'mac_address': interface['mac_address'],
                    'private_ips': interface['private_ips'],
                    'public_ips': PUB_IPS,
                    'resource_group_name': VM['resource_group_name'],
                    'target': VM['target'],
                    'vm_size': VM['vm_size'],
                    'ansible_groups': VM['ansible_groups']
                }
            )

            for security_group in TERRAFORM_SECURITY_GROUPS:
                try:
                    interface['network_security_group_id']
                    if (interface['network_security_group_id'] ==
                            security_group['id']):
                        VM_INFO.update(
                            {
                                'security_groups':
                                security_group['security_groups'],
                            }
                        )
                except KeyError:
                    LOGGER.debug(KeyError)
                    pass

            return VM_INFO


def update_inventory(LOGGER, TERRAFORM_INVENTORY, VM_INFO):
    LOGGER.debug(VM_INFO)
    TERRAFORM_INVENTORY.append(VM_INFO)
