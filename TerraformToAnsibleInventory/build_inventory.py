

def terraform(TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
              TERRAFORM_NETWORK_INTERFACES,
              TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS):
    """Build Terraform inventory structure."""
    for vm in TERRAFORM_VMS:
        pub_ips = []
        _vm = dict()
        if vm['data_type'] not in TERRAFORM_DATA_TYPES:
            TERRAFORM_DATA_TYPES.append(vm['data_type'])

        if vm['data_type'] == 'aws_instance':
            TERRAFORM_INVENTORY.append(vm)

        if vm['data_type'] == 'azurerm_virtual_machine':
            for interface in TERRAFORM_NETWORK_INTERFACES:
                if interface['virtual_machine_id'] == vm['id']:
                    for pub_ip in TERRAFORM_PUBLIC_IPS:
                        if pub_ip['id'] in interface['public_ips']:
                            if pub_ip['ip_address'] not in pub_ips:
                                pub_ips.append(pub_ip['ip_address'])
                        _vm.update(
                            {'inventory_hostname': vm['inventory_hostname'],
                             'data_type': vm['data_type'],
                             'ansible_host': interface['private_ip_address'],
                             'location': vm['location'],
                             'private_ips': interface['private_ips'],
                             'public_ips': pub_ips,
                             'resource_group_name': vm['resource_group_name'],
                             'target': vm['target'],
                             'vm_size': vm['vm_size'],
                             'ansible_groups': vm['ansible_groups']})
                        TERRAFORM_INVENTORY.append(_vm)

        elif vm['data_type'] == 'vsphere_virtual_machine':
            TERRAFORM_INVENTORY.append(vm)
