#! /usr/bin/env python
"""Parses Terraform tfstate to generate Ansible inventory."""

import argparse
import ast
import json
import os
import yaml

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-i", "--inventory", help="Ansible inventory",
                    default="./terraform_inventory.yml")
PARSER.add_argument("-t", "--tfstate", help="Terraform tftstate file",
                    default="./terraform.tfstate")
ARGS = PARSER.parse_args()


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TERRAFORM_INVENTORY = []
TERRAFORM_ANSIBLE_GROUPS = []
TERRAFORM_ANSIBLE_INVENTORY = ("%s/" + ARGS.inventory) % SCRIPT_PATH
TERRAFORM_LOAD_BALANCERS = []
TERRAFORM_NETWORK_INTERFACES = []
TERRAFORM_PUBLIC_IPS = []
TERRAFORM_TFSTATE = ("%s/" + ARGS.tfstate) % SCRIPT_PATH
TERRAFORM_VMS = []

with open(TERRAFORM_TFSTATE) as json_file:
    DATA = json.load(json_file)
    RESOURCES = DATA['modules'][0]['resources']
    for NAME, DATA in RESOURCES.items():
        if DATA['type'] == "azurerm_network_interface":
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

        if DATA['type'] == "azurerm_public_ip":
            public_ip = {}
            raw_attrs = DATA['primary']['attributes']
            public_ip.update({"id": raw_attrs['id'],
                              "ip_address": raw_attrs['ip_address']})
            TERRAFORM_PUBLIC_IPS.append(public_ip)

        if DATA['type'] == "azurerm_lb":
            raw_attrs = DATA['primary']['attributes']
            load_balancer = {}
            public_ip_address = ""
            for pub_ip in TERRAFORM_PUBLIC_IPS:
                public_ip_address_id = raw_attrs['frontend_ip_configuration.0.public_ip_address_id']
                if pub_ip['id'] == public_ip_address_id:
                    public_ip_address = pub_ip['ip_address']
            load_balancer.update({"location": raw_attrs['location'],
                                  "name": raw_attrs['name'],
                                  "public_ip_address": public_ip_address,
                                  "sku": raw_attrs['sku'],
                                  "type": "azurerm_lb"})
            TERRAFORM_LOAD_BALANCERS.append(load_balancer)

        if DATA['type'] == "azurerm_virtual_machine":
            vm = {}
            ansible_groups = []
            raw_attrs = DATA['primary']['attributes']
            if raw_attrs['tags.ansible_groups']:
                groups = ast.literal_eval(raw_attrs['tags.ansible_groups'])
                for group in groups:
                    ansible_groups.append(group)
                    if group not in TERRAFORM_ANSIBLE_GROUPS:
                        TERRAFORM_ANSIBLE_GROUPS.append(group)
            vm.update(
                {"data_type": DATA['type'], "name": raw_attrs['name'],
                 "id": raw_attrs['id'], "location": raw_attrs['location'],
                 "resource_group_name": raw_attrs['resource_group_name'],
                 "vm_size": raw_attrs['vm_size'],
                 "ansible_groups": ansible_groups})
            TERRAFORM_VMS.append(vm)

        if DATA['type'] == "vsphere_virtual_machine":
            vm = {}
            ansible_groups = []
            raw_attrs = DATA['primary']['attributes']
            vm.update(
                {"ansible_host": raw_attrs['network_interface.0.ipv4_address'],
                 "data_type": DATA['type'], "id": raw_attrs['id'],
                 "mac_address": raw_attrs['network_interface.0.mac_address'],
                 "memory": raw_attrs['memory'], "name": raw_attrs['name'],
                 "network_label": raw_attrs['network_interface.0.label'],
                 "uuid": raw_attrs['uuid'], "vcpu": raw_attrs['vcpu'],
                 "ansible_groups": ansible_groups})
            TERRAFORM_VMS.append(vm)

for vm in TERRAFORM_VMS:
    pub_ips = []
    _vm = {}
    if vm['data_type'] == "azurerm_virtual_machine":
        for interface in TERRAFORM_NETWORK_INTERFACES:
            if interface['virtual_machine_id'] == vm['id']:
                for pub_ip in TERRAFORM_PUBLIC_IPS:
                    if pub_ip['id'] in interface['public_ips']:
                        if pub_ip['ip_address'] not in pub_ips:
                            pub_ips.append(pub_ip['ip_address'])
                    _vm.update(
                        {"inventory_hostname": vm['name'], "data_type": vm['data_type'],
                         "ansible_host": interface['private_ip_address'],
                         "location": vm['location'],
                         "private_ips": interface['private_ips'],
                         "public_ips": pub_ips,
                         "resource_group_name": vm['resource_group_name'],
                         "vm_size": vm['vm_size'], "ansible_groups": vm['ansible_groups']})
                    TERRAFORM_INVENTORY.append(_vm)

    elif vm['data_type'] == "vsphere_virtual_machine":
        _vm.update(
            {"inventory_hostname": vm['name'], "data_type": vm['data_type'],
             "ansible_host": vm['ansible_host'],
             "mac_address": vm['mac_address'], "memory": vm['memory'],
             "network_label": vm['network_label'],
             "uuid": vm['uuid'], "vcpu": vm['vcpu'],
             "ansible_groups": vm['ansible_groups']}
        )
        TERRAFORM_INVENTORY.append(_vm)

        # Reset TERRAFORM_VMS for new collection
TERRAFORM_VMS = {}
TERRAFORM_VMS['terraform_vms'] = {}
TERRAFORM_VMS['terraform_vms']['hosts'] = {}

for tag in TERRAFORM_ANSIBLE_GROUPS:
    TERRAFORM_VMS[tag] = {}
    TERRAFORM_VMS[tag]['hosts'] = {}

for vm in TERRAFORM_INVENTORY:
    TERRAFORM_VMS['terraform_vms']['hosts'][vm['inventory_hostname']] = {}
    if vm['data_type'] == "azurerm_virtual_machine":
        TERRAFORM_VMS['terraform_vms']['hosts'][vm['inventory_hostname']].update(
            {"ansible_host": vm['ansible_host'], "data_type": vm['data_type'],
             "location": vm['location'], "private_ips": vm['private_ips'],
             "public_ips": vm['public_ips'],
             "resource_group_name": vm['resource_group_name'],
             "vm_size": vm['vm_size']})
    elif vm['data_type'] == "vsphere_virtual_machine":
        TERRAFORM_VMS['terraform_vms']['hosts'][vm['inventory_hostname']].update(
            {"ansible_host": vm['ansible_host'], "data_type": vm['data_type'],
             "mac_address": vm['mac_address'], "memory": int(vm['memory']),
             "network_label": vm['network_label'], "uuid": vm['uuid'],
             "vcpu": int(vm['vcpu'])}
        )
    for tag in vm['ansible_groups']:
        TERRAFORM_VMS[tag]['hosts'][vm['inventory_hostname']] = {}

TERRAFORM_VMS['terraform_vms']['vars'] = {}
TERRAFORM_VMS['terraform_vms']['vars']['terraform_load_balancers'] = TERRAFORM_LOAD_BALANCERS

TERRAFORM_VMS = yaml.load(json.dumps(TERRAFORM_VMS))

with open(TERRAFORM_ANSIBLE_INVENTORY, 'w') as yaml_file:
    yaml.dump(TERRAFORM_VMS, yaml_file, default_flow_style=False)
