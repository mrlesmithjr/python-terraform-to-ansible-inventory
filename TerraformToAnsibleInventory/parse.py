from . backends.local_backend import load as TerraformLocalBackend
from . backends.consul_backend import load as TerraformConsulBackend
from . parsers.aws_instance import parse as ParseAwsInstance
from . parsers.aws_elb import parse as ParseAwsElb
from . parsers.aws_security_group import parse as ParseAwsSecurityGroup
from . parsers.azurerm_network_interface import parse as ParseAzureNetworkInterface
from . parsers.azurerm_network_security_group import parse as ParseAzureNetworkSecurityGroup
from . parsers.azurerm_public_ip import parse as ParseAzurePublicIp
from . parsers.azurerm_lb import parse as ParseAzureLb
from . parsers.azurerm_virtual_machine import parse as ParseAzureVm
from . parsers.vsphere_virtual_machine import parse as ParsevSphereVm
from . logging_config import setup as LoggingConfigSetup


def terraform_tfstate(ARGS, LOG_LEVEL, TERRAFORM_ANSIBLE_GROUPS,
                      TERRAFORM_NETWORK_INTERFACES,
                      TERRAFORM_LOAD_BALANCERS,
                      TERRAFORM_PUBLIC_IPS,
                      TERRAFORM_TFSTATE,
                      TERRAFORM_VMS, TERRAFORM_SECURITY_GROUPS):
    """Parse terraform.tfstate."""
    DATA = setup_backend(ARGS, LOG_LEVEL, TERRAFORM_TFSTATE)

    parse_data(LOG_LEVEL, DATA, TERRAFORM_VMS, TERRAFORM_NETWORK_INTERFACES,
               TERRAFORM_PUBLIC_IPS, TERRAFORM_LOAD_BALANCERS,
               TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_SECURITY_GROUPS)


def setup_backend(ARGS, LOG_LEVEL, TERRAFORM_TFSTATE):
    LOGGER = LoggingConfigSetup(LOG_LEVEL)

    if ARGS.backend == 'local':
        LOGGER.info('Parsing Terraform backend: %s' % ARGS.backend)
        DATA = TerraformLocalBackend(LOG_LEVEL, TERRAFORM_TFSTATE)

    elif ARGS.backend == 'consul':
        LOGGER.info('Parsing Terraform backend: %s' % ARGS.backend)
        DATA = TerraformConsulBackend(ARGS, LOG_LEVEL)

    return DATA


def parse_data(LOG_LEVEL, DATA, TERRAFORM_VMS, TERRAFORM_NETWORK_INTERFACES,
               TERRAFORM_PUBLIC_IPS, TERRAFORM_LOAD_BALANCERS,
               TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_SECURITY_GROUPS):
    """Now we parse all of the data collected from our backends."""
    DATA_MODULES = DATA['modules']
    LOGGER = LoggingConfigSetup(LOG_LEVEL)

    if len(DATA_MODULES) > 1:
        LOGGER.info('%s module elements found for processing.' %
                    len(DATA_MODULES))
    else:
        LOGGER.info('%s module element found for processing.' %
                    len(DATA_MODULES))

    for ELEMENT in range(len(DATA_MODULES)):
        RESOURCES = DATA_MODULES[ELEMENT]['resources']

        # We first need to iterate over resources to collect all Public IP's
        # This ensures that all public IP information is collected prior to
        # iterating over LB's for correlation
        public_ips(RESOURCES, LOGGER, LOG_LEVEL, TERRAFORM_PUBLIC_IPS)

        # We next need to iterate over resources to collect all LB information
        # This ensures that all LB information is collected prior to
        # iterating over additional resources, and also ensure correlation
        # between Public IPs and LB's
        load_balancers(RESOURCES, LOGGER, LOG_LEVEL,
                       TERRAFORM_LOAD_BALANCERS, TERRAFORM_PUBLIC_IPS)

        # We next iterate over any security groups to collect info
        security_groups(RESOURCES, LOGGER, LOG_LEVEL,
                        TERRAFORM_SECURITY_GROUPS)

        # Now we can iterate over the remaining resources
        remaining_resources(RESOURCES, LOGGER, LOG_LEVEL,
                            TERRAFORM_VMS, TERRAFORM_NETWORK_INTERFACES,
                            TERRAFORM_ANSIBLE_GROUPS)


def public_ips(RESOURCES, LOGGER, LOG_LEVEL, TERRAFORM_PUBLIC_IPS):
    """Captures Azure public IPs."""
    for NAME, RESOURCE in RESOURCES.items():
        if RESOURCE['type'] == 'azurerm_public_ip':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAzurePublicIp(LOG_LEVEL, RESOURCE, TERRAFORM_PUBLIC_IPS)


def load_balancers(RESOURCES, LOGGER, LOG_LEVEL, TERRAFORM_LOAD_BALANCERS,
                   TERRAFORM_PUBLIC_IPS):
    """Captures LB configurations."""
    for NAME, RESOURCE in RESOURCES.items():
        if RESOURCE['type'] == 'azurerm_lb':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAzureLb(LOG_LEVEL, RESOURCE, TERRAFORM_LOAD_BALANCERS,
                         TERRAFORM_PUBLIC_IPS)

        elif RESOURCE['type'] == 'aws_elb':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAwsElb(LOG_LEVEL, RESOURCE, TERRAFORM_LOAD_BALANCERS,
                        TERRAFORM_PUBLIC_IPS)


def security_groups(RESOURCES, LOGGER, LOG_LEVEL, TERRAFORM_SECURITY_GROUPS):
    """Captures security groups."""
    for NAME, RESOURCE in RESOURCES.items():
        if RESOURCE['type'] == 'azurerm_network_security_group':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAzureNetworkSecurityGroup(
                LOG_LEVEL, RESOURCE, TERRAFORM_SECURITY_GROUPS)

        elif RESOURCE['type'] == 'aws_security_group':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAwsSecurityGroup(
                LOG_LEVEL, RESOURCE, TERRAFORM_SECURITY_GROUPS)


def remaining_resources(RESOURCES, LOGGER, LOG_LEVEL, TERRAFORM_VMS,
                        TERRAFORM_NETWORK_INTERFACES,
                        TERRAFORM_ANSIBLE_GROUPS):
    """Process remaining resources (VMs and etc.)."""
    for NAME, RESOURCE in RESOURCES.items():
        if RESOURCE['type'] == 'aws_instance':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAwsInstance(LOG_LEVEL, RESOURCE, NAME, TERRAFORM_VMS)

        elif RESOURCE['type'] == 'azurerm_network_interface':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAzureNetworkInterface(
                LOG_LEVEL, RESOURCE, TERRAFORM_NETWORK_INTERFACES)

        elif RESOURCE['type'] == 'azurerm_virtual_machine':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParseAzureVm(
                LOG_LEVEL, NAME, RESOURCE, TERRAFORM_ANSIBLE_GROUPS,
                TERRAFORM_VMS)

        elif RESOURCE['type'] == 'vsphere_virtual_machine':
            LOGGER.info('Processing resource type: %s' % RESOURCE['type'])
            ParsevSphereVm(LOG_LEVEL, RESOURCE, TERRAFORM_VMS)
