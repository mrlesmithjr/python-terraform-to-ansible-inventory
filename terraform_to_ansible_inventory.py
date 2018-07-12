#! /usr/bin/env python

"""Parses Terraform tfstate to generate Ansible inventory."""

import argparse
import ast
import json
import os
import yaml

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr


def main():
    """The main execution of script."""
    ARGS = parse_args()

    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    TERRAFORM_ANSIBLE_GROUPS = []
    TERRAFORM_ANSIBLE_INVENTORY = ("%s/" + ARGS.inventory) % SCRIPT_PATH
    TERRAFORM_DATA_TYPES = []
    TERRAFORM_INVENTORY = []
    TERRAFORM_LOAD_BALANCERS = []
    TERRAFORM_NETWORK_INTERFACES = []
    TERRAFORM_PUBLIC_IPS = []
    TERRAFORM_TFSTATE = ("%s/" + ARGS.tfstate) % SCRIPT_PATH
    TERRAFORM_VMS = []

    parse_terraform_tfstate(TERRAFORM_ANSIBLE_GROUPS,
                            TERRAFORM_NETWORK_INTERFACES,
                            TERRAFORM_LOAD_BALANCERS,
                            TERRAFORM_PUBLIC_IPS,
                            TERRAFORM_TFSTATE,
                            TERRAFORM_VMS)

    build_terraform_inventory(TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
                              TERRAFORM_NETWORK_INTERFACES,
                              TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS)

    generate_terraform_inventory(
        TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_ANSIBLE_INVENTORY,
        TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY, TERRAFORM_LOAD_BALANCERS)


def parse_args():
    """Parse command line arguments."""
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-i", "--inventory", help="Ansible inventory",
                        default="./terraform_inventory.yml")
    PARSER.add_argument("-t", "--tfstate", help="Terraform tftstate file",
                        default="./terraform.tfstate")
    ARGS = PARSER.parse_args()
    return ARGS


def parse_terraform_tfstate(TERRAFORM_ANSIBLE_GROUPS,
                            TERRAFORM_NETWORK_INTERFACES,
                            TERRAFORM_LOAD_BALANCERS,
                            TERRAFORM_PUBLIC_IPS,
                            TERRAFORM_TFSTATE,
                            TERRAFORM_VMS):
    """Parse terraform.tfstate."""
    with open(TERRAFORM_TFSTATE) as json_file:
        DATA = json.load(json_file)
        DATA_MODULES = DATA['modules']
        print "Processing %s different module elements." % len(DATA_MODULES)
        for ELEMENT in range(len(DATA_MODULES)):
            RESOURCES = DATA_MODULES[ELEMENT]['resources']
            for NAME, DATA in RESOURCES.items():
                if DATA['type'] == "aws_instance":
                    aws_instance(DATA, NAME, TERRAFORM_VMS)

                if DATA['type'] == "azurerm_network_interface":
                    azurerm_network_interface(
                        DATA, TERRAFORM_NETWORK_INTERFACES)

                elif DATA['type'] == "azurerm_public_ip":
                    azurerm_public_ip(DATA, TERRAFORM_PUBLIC_IPS)

                elif DATA['type'] == "azurerm_lb":
                    azurerm_lb(DATA, TERRAFORM_LOAD_BALANCERS,
                               TERRAFORM_PUBLIC_IPS)

                elif DATA['type'] == "azurerm_virtual_machine":
                    azurerm_virtual_machine(
                        DATA, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS)

                elif DATA['type'] == "vsphere_virtual_machine":
                    vsphere_virtual_machine(DATA, TERRAFORM_VMS)


def aws_instance(DATA, NAME, TERRAFORM_VMS):
    """Populate AWS VM info."""
    vm = {}
    ansible_groups = []
    raw_attrs = DATA['primary']['attributes']
    vm_name = NAME.split('.')[1]
    vm.update({"ansible_host": raw_attrs['private_ip'],
               "data_type": DATA['type'], "inventory_hostname": vm_name,
               "ami": raw_attrs['ami'],
               "ansible_groups": ansible_groups,
               "availability_zone": raw_attrs['availability_zone'],
               "instance_type": raw_attrs['instance_type'],
               "private_ip": raw_attrs['private_ip'],
               "public_ip": raw_attrs['public_ip']})
    TERRAFORM_VMS.append(vm)


def azurerm_network_interface(DATA, TERRAFORM_NETWORK_INTERFACES):
    """Populate Azure network interface info."""
    interface = {}
    private_ips = []
    public_ips = []
    raw_attrs = DATA['primary']['attributes']
    num_ips = int(raw_attrs['ip_configuration.#'])
    for count in xrange(num_ips):
        private_ips.append(
            raw_attrs['private_ip_addresses.%s' % count])
        public_ips.append(
            raw_attrs['ip_configuration.%s.public_ip_address_id' % count])
    interface.update({"virtual_machine_id": raw_attrs['virtual_machine_id'],
                      "mac_address": raw_attrs['mac_address'],
                      "private_ip_address": raw_attrs['private_ip_address'],
                      "private_ips": private_ips,
                      "public_ips": public_ips})
    TERRAFORM_NETWORK_INTERFACES.append(interface)


def azurerm_public_ip(DATA, TERRAFORM_PUBLIC_IPS):
    """Populate Azure public IP info."""
    public_ip = {}
    raw_attrs = DATA['primary']['attributes']
    public_ip.update({"id": raw_attrs['id'],
                      "ip_address": raw_attrs['ip_address']})
    TERRAFORM_PUBLIC_IPS.append(public_ip)


def azurerm_lb(DATA, TERRAFORM_LOAD_BALANCERS, TERRAFORM_PUBLIC_IPS):
    """Populate Azure LB info."""
    raw_attrs = DATA['primary']['attributes']
    load_balancer = {}
    public_ip_address = ""
    for pub_ip in TERRAFORM_PUBLIC_IPS:
        public_ip_address_id = (
            raw_attrs['frontend_ip_configuration.0.public_ip_address_id'])
        if pub_ip['id'] == public_ip_address_id:
            public_ip_address = pub_ip['ip_address']
    load_balancer.update({"location": raw_attrs['location'],
                          "name": raw_attrs['name'],
                          "public_ip_address": public_ip_address,
                          "sku": raw_attrs['sku'],
                          "type": "azurerm_lb"})
    TERRAFORM_LOAD_BALANCERS.append(load_balancer)


def azurerm_virtual_machine(DATA, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS):
    """Populate Azure VM info."""
    vm = {}
    raw_attrs = DATA['primary']['attributes']
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
        {"data_type": DATA['type'], "inventory_hostname": raw_attrs['name'],
         "id": raw_attrs['id'], "location": raw_attrs['location'],
         "resource_group_name": raw_attrs['resource_group_name'],
         "target": DATA['type'] + "." + raw_attrs['name'],
         "vm_size": raw_attrs['vm_size'],
         "ansible_groups": ansible_groups})
    TERRAFORM_VMS.append(vm)


def vsphere_virtual_machine(DATA, TERRAFORM_VMS):
    """Populate vSphere VM info."""
    vm = {}
    ansible_groups = []
    raw_attrs = DATA['primary']['attributes']
    vm.update(
        {"ansible_host": raw_attrs['network_interface.0.ipv4_address'],
         "data_type": DATA['type'], "id": raw_attrs['id'],
         "mac_address": raw_attrs['network_interface.0.mac_address'],
         "memory": raw_attrs['memory'], "inventory_hostname": raw_attrs['name'],
         "network_label": raw_attrs['network_interface.0.label'],
         "target": DATA['type'] + "." + raw_attrs['name'],
         "uuid": raw_attrs['uuid'], "vcpu": raw_attrs['vcpu'],
         "ansible_groups": ansible_groups})
    TERRAFORM_VMS.append(vm)


def build_terraform_inventory(TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
                              TERRAFORM_NETWORK_INTERFACES,
                              TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS):
    """Build Terraform inventory structure."""
    for vm in TERRAFORM_VMS:
        pub_ips = []
        _vm = {}
        if vm['data_type'] not in TERRAFORM_DATA_TYPES:
            TERRAFORM_DATA_TYPES.append(vm['data_type'])

        if vm['data_type'] == "aws_instance":
            TERRAFORM_INVENTORY.append(vm)

        if vm['data_type'] == "azurerm_virtual_machine":
            for interface in TERRAFORM_NETWORK_INTERFACES:
                if interface['virtual_machine_id'] == vm['id']:
                    for pub_ip in TERRAFORM_PUBLIC_IPS:
                        if pub_ip['id'] in interface['public_ips']:
                            if pub_ip['ip_address'] not in pub_ips:
                                pub_ips.append(pub_ip['ip_address'])
                        _vm.update(
                            {"inventory_hostname": vm['inventory_hostname'],
                             "data_type": vm['data_type'],
                             "ansible_host": interface['private_ip_address'],
                             "location": vm['location'],
                             "private_ips": interface['private_ips'],
                             "public_ips": pub_ips,
                             "resource_group_name": vm['resource_group_name'],
                             "target": vm['target'],
                             "vm_size": vm['vm_size'],
                             "ansible_groups": vm['ansible_groups']})
                        TERRAFORM_INVENTORY.append(_vm)

        elif vm['data_type'] == "vsphere_virtual_machine":
            TERRAFORM_INVENTORY.append(vm)


def generate_terraform_inventory(TERRAFORM_ANSIBLE_GROUPS,
                                 TERRAFORM_ANSIBLE_INVENTORY,
                                 TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
                                 TERRAFORM_LOAD_BALANCERS):
    """Generate Terraform inventory for Ansible and write to inventory file."""
    # Reset TERRAFORM_VMS for new collection
    TERRAFORM_VMS = {}

    for group in TERRAFORM_ANSIBLE_GROUPS:
        TERRAFORM_VMS[group] = {}
        TERRAFORM_VMS[group]['hosts'] = {}

    for data_type in TERRAFORM_DATA_TYPES:
        TERRAFORM_VMS[data_type] = {}
        TERRAFORM_VMS[data_type]['hosts'] = {}

    TERRAFORM_VMS['terraform_vms'] = {}
    TERRAFORM_VMS['terraform_vms']['hosts'] = {}

    for vm in TERRAFORM_INVENTORY:
        TERRAFORM_VMS[vm['data_type']]['hosts'].update(
            {vm['inventory_hostname']: {}})

        TERRAFORM_VMS['terraform_vms']['hosts'][vm['inventory_hostname']] = vm

        for group in vm['ansible_groups']:
            TERRAFORM_VMS[group]['hosts'][vm['inventory_hostname']] = {}

    TERRAFORM_VMS['terraform_vms']['vars'] = {}
    if TERRAFORM_LOAD_BALANCERS != []:
        TERRAFORM_VMS['terraform_vms']['vars'].update(
            {"terraform_load_balancers": TERRAFORM_LOAD_BALANCERS})

    TERRAFORM_VMS = yaml.load(json.dumps(TERRAFORM_VMS))

    with open(TERRAFORM_ANSIBLE_INVENTORY, 'w') as yaml_file:
        yaml.dump(TERRAFORM_VMS, yaml_file, default_flow_style=False)


if __name__ == "__main__":
    main()
