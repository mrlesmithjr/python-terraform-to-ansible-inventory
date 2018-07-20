# python-terraform-to-ansible-inventory

This package is for consuming [Terraform State](https://www.terraform.io/docs/state/),
parsing the data, and then generating a functional Ansible inventory which can
then be consumed by Ansible.

## Ansible Groups

By default all VMs are placed into the Ansible group `terraform_vms`, however
you can also define additional Ansible groups by leveraging tags on your VM
resources. By default this will currently look for `tags.ansible_groups` which
can be defined on a resource as below:

> NOTE: Currently only limited testing on AWS, Azure, and vSphere resources.

```json
tags {
  ansible_groups = "['test', 'cluster']"
}
```

## Installation

### Manual

You can manually install this package by executing the following:

```bash
python setup.py install
```

### Using pip

You can also install using `pip`:

```bash
pip install TerraformToAnsibleInventory
```

After installation, you can then use this package from anywhere within your
terminal session.

```bash
TerraformToAnsibleInventory -t terraform.tfstate.vsphere -i terraform_inventory.yml
```

## Supported Terraform Backends

The following backends are currently supported for consumption.

-   local - A local `terraform.tfstate` file present where executing from.
-   consul - A Consul environment in which Terraform state is stored.

## Execution

You can view help to familiarize yourself with the options available for usage
by executing:

```bash
TerraformToAnsibleInventory --help
...
usage: TerraformToAnsibleInventory [-h] [-b {local,consul}] [-cH CONSULHOST] [-cKV CONSULKV]
                  [-cP CONSULPORT] [-cS {http,https}] [-i INVENTORY]
                  [-t TFSTATE]

optional arguments:
  -h, --help            show this help message and exit
  -b {local,consul}, --backend {local,consul}
                        Define which Terraform backend to parse
  -cH CONSULHOST, --consulHost CONSULHOST
                        Define Consul host when using Consul backend
  -cKV CONSULKV, --consulKV CONSULKV
                        Define Consul KV Pair to query. Ex. Azure/Test
  -cP CONSULPORT, --consulPort CONSULPORT
                        Define Consul host port
  -cS {http,https}, --consulScheme {http,https}
                        Define Consul connection scheme.
  -i INVENTORY, --inventory INVENTORY
                        Ansible inventory
  -t TFSTATE, --tfstate TFSTATE
                        Terraform tftstate file
```

### Using A Local Backend

```bash
TerraformToAnsibleInventory -t terraform.tfstate -i terraform_inventory.yml
```

### Using A Consul Backend

```bash
TerraformToAnsibleInventory -b consul -cH consul.example.org -cKV Azure/Test -i terraform_inventory.yml
```

## Example Inventories

### AWS

```yaml
terraform_vms:
  hosts:
    ubuntu_zesty:
      ami: ami-6b7f610f
      ansible_host: 172.31.0.208
      availability_zone: eu-west-2a
      data_type: aws_instance
      instance_type: t2.micro
      private_ip: 172.31.0.208
      public_ip: 52.56.204.79
  vars: {}
```

### Azure

```yaml
terraform_vms:
  hosts:
    Jumphost:
      ansible_host: 10.0.2.4
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.4
      public_ips:
      - 40.117.254.203
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm0:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm1:
      ansible_host: 10.0.2.7
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.7
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm2:
      ansible_host: 10.0.2.5
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.5
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
  vars:
    terraform_load_balancers:
    - location: eastus
      name: TestLoadBalancer
      public_ip_address: 40.76.73.163
      sku: Basic
      type: azurerm_lb
```

### vSphere

```yaml
terraform_vms:
  hosts:
    docker-lb-01.lab.etsbv.internal:
      ansible_host: 10.0.102.163
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:9c:b3
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422a4adb-e7d3-ea74-a69a-3ff10c13063f
      vcpu: 1
    docker-lb-02.lab.etsbv.internal:
      ansible_host: 10.0.102.160
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:f8:25
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422adcf8-347a-e9a5-e113-00114c1d2de9
      vcpu: 1
    docker-mgr-01.lab.etsbv.internal:
      ansible_host: 10.0.102.171
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:a9:c0
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422abe05-4483-88f8-34b7-e354fdc7a211
      vcpu: 1
    docker-mgr-02.lab.etsbv.internal:
      ansible_host: 10.0.102.166
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:ba:a0
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422a5d74-4de2-1df8-646b-ca62311f98ab
      vcpu: 1
    docker-mgr-03.lab.etsbv.internal:
      ansible_host: 10.0.102.179
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e3:06
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422a8d34-68f7-a7be-9c6a-18949ce809ed
      vcpu: 1
    docker-storage-01.lab.etsbv.internal:
      ansible_host: 10.0.102.162
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:5f:cb
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422a264a-0816-60ff-475c-23af6c0b9d0e
      vcpu: 1
    docker-storage-02.lab.etsbv.internal:
      ansible_host: 10.0.102.178
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:01:a0
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422ad693-162f-1c32-b90c-eee1b0a73d2b
      vcpu: 1
    docker-wrk-01.lab.etsbv.internal:
      ansible_host: 10.0.102.155
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e4:93
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a87fe-baa2-75d6-e666-36c15f351269
      vcpu: 1
    docker-wrk-02.lab.etsbv.internal:
      ansible_host: 10.0.102.201
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e0:36
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a49e3-746c-b550-189c-0e0179c60418
      vcpu: 1
    docker-wrk-03.lab.etsbv.internal:
      ansible_host: 10.0.102.207
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:6b:d5
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a809a-0cd2-cd84-756b-0822bc3f813a
      vcpu: 1
    docker-wrk-04.lab.etsbv.internal:
      ansible_host: 10.0.102.183
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:b5:43
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422aae57-67e8-50d8-66f6-3a11bdc87a78
      vcpu: 1
```

### Mixed

```yaml
terraform_vms:
  hosts:
    Jumphost:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips:
      - 40.117.254.203
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm0:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm1:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm2:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    docker-lb-01.lab.etsbv.internal:
      ansible_host: 10.0.102.163
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:9c:b3
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422a4adb-e7d3-ea74-a69a-3ff10c13063f
      vcpu: 1
    docker-lb-02.lab.etsbv.internal:
      ansible_host: 10.0.102.160
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:f8:25
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422adcf8-347a-e9a5-e113-00114c1d2de9
      vcpu: 1
    docker-mgr-01.lab.etsbv.internal:
      ansible_host: 10.0.102.171
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:a9:c0
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422abe05-4483-88f8-34b7-e354fdc7a211
      vcpu: 1
    docker-mgr-02.lab.etsbv.internal:
      ansible_host: 10.0.102.166
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:ba:a0
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422a5d74-4de2-1df8-646b-ca62311f98ab
      vcpu: 1
    docker-mgr-03.lab.etsbv.internal:
      ansible_host: 10.0.102.179
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e3:06
      memory: 1024
      network_label: VSS-VLAN-102
      uuid: 422a8d34-68f7-a7be-9c6a-18949ce809ed
      vcpu: 1
    docker-storage-01.lab.etsbv.internal:
      ansible_host: 10.0.102.162
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:5f:cb
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422a264a-0816-60ff-475c-23af6c0b9d0e
      vcpu: 1
    docker-storage-02.lab.etsbv.internal:
      ansible_host: 10.0.102.178
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:01:a0
      memory: 512
      network_label: VSS-VLAN-102
      uuid: 422ad693-162f-1c32-b90c-eee1b0a73d2b
      vcpu: 1
    docker-wrk-01.lab.etsbv.internal:
      ansible_host: 10.0.102.155
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e4:93
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a87fe-baa2-75d6-e666-36c15f351269
      vcpu: 1
    docker-wrk-02.lab.etsbv.internal:
      ansible_host: 10.0.102.201
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:e0:36
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a49e3-746c-b550-189c-0e0179c60418
      vcpu: 1
    docker-wrk-03.lab.etsbv.internal:
      ansible_host: 10.0.102.207
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:6b:d5
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422a809a-0cd2-cd84-756b-0822bc3f813a
      vcpu: 1
    docker-wrk-04.lab.etsbv.internal:
      ansible_host: 10.0.102.183
      data_type: vsphere_virtual_machine
      mac_address: 00:50:56:aa:b5:43
      memory: 4096
      network_label: VSS-VLAN-102
      uuid: 422aae57-67e8-50d8-66f6-3a11bdc87a78
      vcpu: 1
  vars:
    terraform_load_balancers:
    - location: eastus
      name: TestLoadBalancer
      public_ip_address: 40.76.73.163
      sku: Basic
      type: azurerm_lb
```

### Azure Using Tags For Ansible Groups

```yaml
cluster:
  hosts:
    acctvm0: {}
    acctvm1: {}
    acctvm2: {}
jumphosts:
  hosts:
    Jumphost: {}
terraform_vms:
  hosts:
    Jumphost:
      ansible_host: 10.0.2.4
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.4
      public_ips:
      - 40.117.254.203
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm0:
      ansible_host: 10.0.2.6
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.6
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm1:
      ansible_host: 10.0.2.7
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.7
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
    acctvm2:
      ansible_host: 10.0.2.5
      data_type: azurerm_virtual_machine
      location: eastus
      private_ips:
      - 10.0.2.5
      public_ips: []
      resource_group_name: acctestrg
      vm_size: Standard_B1s
  vars:
    terraform_load_balancers:
    - location: eastus
      name: TestLoadBalancer
      public_ip_address: 40.76.73.163
      sku: Basic
      type: azurerm_lb
test:
  hosts:
    Jumphost: {}
    acctvm0: {}
    acctvm1: {}
    acctvm2: {}
```

### Groups Created By Data Types

You can also execute Ansible against a specific type by using these groups.

> NOTE: Snippet below excludes all of the additional groups that are created to
> keep example clean.

```yaml
aws_instance:
  hosts:
    ubuntu_zesty: {}
azurerm_virtual_machine:
  hosts:
    Jumphost: {}
    acctvm0: {}
    acctvm1: {}
    acctvm2: {}
vsphere_virtual_machine:
  hosts:
    docker-lb-01.lab.etsbv.internal: {}
    docker-lb-02.lab.etsbv.internal: {}
    docker-mgr-01.lab.etsbv.internal: {}
    docker-mgr-02.lab.etsbv.internal: {}
    docker-mgr-03.lab.etsbv.internal: {}
    docker-storage-01.lab.etsbv.internal: {}
    docker-storage-02.lab.etsbv.internal: {}
    docker-wrk-01.lab.etsbv.internal: {}
    docker-wrk-02.lab.etsbv.internal: {}
    docker-wrk-03.lab.etsbv.internal: {}
    docker-wrk-04.lab.etsbv.internal: {}
```

## Ansible Terraform Module Usage

When using the terraform Ansible module you have the ability to specify
`target` which can be a single target or a list of targets. This is particularly
useful when your infrastructure is already provisioned and you would like to
destroy targets. We now add the actual Terraform target as a host variable named
`target` as seen in the example below:

```yaml
terraform_vms:
  hosts:
    acctvm0:
      ansible_groups:
      - test
      - consul_cluster
      ansible_host: 10.0.2.4
      data_type: azurerm_virtual_machine
      inventory_hostname: acctvm0
      location: eastus
      private_ips:
      - 10.0.2.4
      public_ips: []
      resource_group_name: acctestrg
      target: azurerm_virtual_machine.acctvm0
      vm_size: Standard_B1s
    acctvm1:
      ansible_groups:
      - test
      - consul_cluster
      ansible_host: 10.0.2.7
      data_type: azurerm_virtual_machine
      inventory_hostname: acctvm1
      location: eastus
      private_ips:
      - 10.0.2.7
      public_ips: []
      resource_group_name: acctestrg
      target: azurerm_virtual_machine.acctvm1
      vm_size: Standard_B1s
```

Now if you would like to leverage the Terraform Ansible module to specifically
target a resource we can do so as seen below:

`playbook.yml`:

```yaml
---
- hosts: localhost
  gather_facts: false
  become: false
  vars:
    scripts_dir: ../../scripts
    terraform_destroy: false
    terraform_destroy_vms: []
    terraform_project_path: ../../Terraform
  tasks:
    - name: Execute Terraform (Provision)
      terraform:
        project_path: "{{ terraform_project_path }}"
        state: present
      register: _terraform_execution_provision
      when: not terraform_destroy

    - name: Execute Terraform (Destroy VMs Only)
      terraform:
        project_path: "{{ terraform_project_path }}"
        state: absent
        targets: "{{ terraform_destroy_vms | map('extract', hostvars, ['target']) | join(',') }}"
      register: _terraform_execution_destroy
      when: >
            terraform_destroy_vms != [] and
            terraform_destroy
```

Playbook execution:

First run in check mode to ensure your results are as expected.

```bash
ansible-playbook -i Ansible/inventory Ansible/playbooks/terraform.yml --extra-vars "{'terraform_destroy': true,'terraform_destroy_vms': ['acctvm0', 'acctvm1']}" --check
...
TASK [Terraform Results (Destroy VMs Only)] ****************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "_terraform_execution_destroy": {
        "changed": false,
        "command": "/usr/local/bin/terraform destroy -no-color -force -lock=true -target azurerm_virtual_machine.acctvm0 -target azurerm_virtual_machine.acctvm1",
        "failed": false,
        "outputs": {
        },
        "state": "absent",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "",
        "stdout_lines": []
    }
}
```

Now run normally after validating in check mode.

```bash
ansible-playbook -i Ansible/inventory Ansible/playbooks/terraform.yml --extra-vars "{'terraform_destroy': true,'terraform_destroy_vms': ['acctvm0', 'acctvm1']}"
```

If you would like to destroy all VMs in an Ansible group:

```bash
ansible-playbook -i Ansible/inventory Ansible/playbooks/terraform.yml --extra-vars "{'terraform_destroy': true,'terraform_destroy_vms': '{{ groups.consul_cluster }}'}" --check
```

## License

MIT

## Author Information

Larry Smith Jr.

-   [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
-   [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
-   <mailto:mrlesmithjr@gmail.com>
