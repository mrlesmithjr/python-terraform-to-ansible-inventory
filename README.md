# 

This script will ingest a Terraform tfstate file and generate an Ansible
inventory for consumption.

## Execution

```bash
./terraform_to_ansible_inventory.py -t Terraform/terraform.tfstate -i Ansible/inventory/terraform_inventory.yml
```

## Example Inventories

### Azure

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

## License

MIT

## Author Information

Larry Smith Jr.

-   [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
-   [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
-   <mailto:mrlesmithjr@gmail.com>
