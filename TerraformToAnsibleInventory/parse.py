from . backends.local_backend import load as TerraformLocalBackend
from . backends.consul_backend import load as TerraformConsulBackend
from . parsers.aws_instance import parse as ParseAwsInstance
from . parsers.azurerm_network_interface import parse as ParseAzureNetworkInterface
from . parsers.azurerm_public_ip import parse as ParseAzurePublicIp
from . parsers.azurerm_lb import parse as ParseAzureLb
from . parsers.azurerm_virtual_machine import parse as ParseAzureVm
from . parsers.vsphere_virtual_machine import parse as ParsevSphereVm


def terraform_tfstate(ARGS, TERRAFORM_ANSIBLE_GROUPS,
                      TERRAFORM_NETWORK_INTERFACES,
                      TERRAFORM_LOAD_BALANCERS,
                      TERRAFORM_PUBLIC_IPS,
                      TERRAFORM_TFSTATE,
                      TERRAFORM_VMS):
    """Parse terraform.tfstate."""

    if ARGS.backend == 'local':
        DATA = TerraformLocalBackend(TERRAFORM_TFSTATE)
    elif ARGS.backend == 'consul':
        DATA = TerraformConsulBackend(ARGS)

    parse_data(DATA, TERRAFORM_VMS, TERRAFORM_NETWORK_INTERFACES,
               TERRAFORM_PUBLIC_IPS, TERRAFORM_LOAD_BALANCERS,
               TERRAFORM_ANSIBLE_GROUPS)


def parse_data(DATA, TERRAFORM_VMS, TERRAFORM_NETWORK_INTERFACES,
               TERRAFORM_PUBLIC_IPS, TERRAFORM_LOAD_BALANCERS,
               TERRAFORM_ANSIBLE_GROUPS):
    """Now we parse all of the data collected from our backends."""
    DATA_MODULES = DATA['modules']
    print "Processing %s different module elements." % len(DATA_MODULES)
    for ELEMENT in range(len(DATA_MODULES)):
        RESOURCES = DATA_MODULES[ELEMENT]['resources']

        # We first need to iterate over resources to collect all Public IP's
        # This ensures that all public IP information is collected prior to
        # iterating over LB's for correlation
        for NAME, RESOURCE in RESOURCES.items():
            if RESOURCE['type'] == 'azurerm_public_ip':
                ParseAzurePublicIp(RESOURCE, TERRAFORM_PUBLIC_IPS)

        # We next need to iterate over resources to collect all LB information
        # This ensures that all LB information is collected prior to
        # iterating over additional resources, and also ensure correlation
        # between Public IPs and LB's
        for NAME, RESOURCE in RESOURCES.items():
            if RESOURCE['type'] == 'azurerm_lb':
                ParseAzureLb(RESOURCE, TERRAFORM_LOAD_BALANCERS,
                             TERRAFORM_PUBLIC_IPS)

        # Now we can iterate over the remaining resources
        for NAME, RESOURCE in RESOURCES.items():
            if RESOURCE['type'] == 'aws_instance':
                ParseAwsInstance(RESOURCE, NAME, TERRAFORM_VMS)

            elif RESOURCE['type'] == 'azurerm_network_interface':
                ParseAzureNetworkInterface(
                    RESOURCE, TERRAFORM_NETWORK_INTERFACES)

            elif RESOURCE['type'] == 'azurerm_virtual_machine':
                ParseAzureVm(
                    RESOURCE, TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_VMS)

            elif RESOURCE['type'] == 'vsphere_virtual_machine':
                ParsevSphereVm(RESOURCE, TERRAFORM_VMS)
