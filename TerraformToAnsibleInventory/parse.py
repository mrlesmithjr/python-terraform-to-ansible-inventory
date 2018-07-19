import json
from TerraformToAnsibleInventory.parsers.aws_instance import (
    parse as ParseAwsInstance)
from TerraformToAnsibleInventory.parsers.azurerm_network_interface import (
    parse as ParseAzureNetworkInterface)
from TerraformToAnsibleInventory.parsers.azurerm_public_ip import (
    parse as ParseAzurePublicIp)
from TerraformToAnsibleInventory.parsers.azurerm_lb import (
    parse as ParseAzureLb)
from TerraformToAnsibleInventory.parsers.azurerm_virtual_machine import (
    parse as ParseAzureVm)
from TerraformToAnsibleInventory.parsers.vsphere_virtual_machine import (
    parse as ParsevSphereVm)


def terraform_tfstate(TERRAFORM_ANSIBLE_GROUPS,
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
                if DATA['type'] == 'aws_instance':
                    ParseAwsInstance(DATA, NAME, TERRAFORM_VMS)

                elif DATA['type'] == 'azurerm_network_interface':
                    ParseAzureNetworkInterface(
                        DATA, TERRAFORM_NETWORK_INTERFACES)

                elif DATA['type'] == 'azurerm_public_ip':
                    ParseAzurePublicIp(DATA, TERRAFORM_PUBLIC_IPS)

                elif DATA['type'] == 'azurerm_lb':
                    ParseAzureLb(DATA, TERRAFORM_LOAD_BALANCERS,
                                 TERRAFORM_PUBLIC_IPS)

                elif DATA['type'] == 'azurerm_virtual_machine':
                    ParseAzureVm(
                        DATA, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS)

                elif DATA['type'] == 'vsphere_virtual_machine':
                    ParsevSphereVm(DATA, TERRAFORM_VMS)
