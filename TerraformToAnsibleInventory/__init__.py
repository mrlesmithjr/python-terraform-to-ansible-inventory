import os
from . args import parse as ArgsParse
from . parse import terraform_tfstate as ParseTerraformTfstate
from . build_inventory import terraform as BuildTerraformInventory
from . generate_inventory import ansible as GenerateAnsibleInventory
from . logging_config import setup as LoggingConfigSetup

ARGS = ArgsParse()
LOG_LEVEL = ARGS.logLevel
LOGGER = LoggingConfigSetup(LOG_LEVEL)

CWD = os.getcwd()
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TERRAFORM_ANSIBLE_GROUPS = []
TERRAFORM_ANSIBLE_INVENTORY = ('%s/' + ARGS.inventory) % CWD
TERRAFORM_DATA_TYPES = []
TERRAFORM_INVENTORY = []
TERRAFORM_LOAD_BALANCERS = []
TERRAFORM_NETWORK_INTERFACES = []
TERRAFORM_SECURITY_GROUPS = []
TERRAFORM_PUBLIC_IPS = []
TERRAFORM_TFSTATE = ('%s/' + ARGS.tfstate) % CWD
TERRAFORM_VMS = []

LOGGER.info('Beginning Terraform State parsing.')
ParseTerraformTfstate(ARGS, LOG_LEVEL, TERRAFORM_ANSIBLE_GROUPS,
                      TERRAFORM_NETWORK_INTERFACES,
                      TERRAFORM_LOAD_BALANCERS,
                      TERRAFORM_PUBLIC_IPS,
                      TERRAFORM_TFSTATE,
                      TERRAFORM_VMS, TERRAFORM_SECURITY_GROUPS)

LOGGER.info('Beginning to build Terraform inventory.')
BuildTerraformInventory(LOG_LEVEL, TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
                        TERRAFORM_NETWORK_INTERFACES,
                        TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS,
                        TERRAFORM_SECURITY_GROUPS)

LOGGER.info('Generating inventory.')
GenerateAnsibleInventory(LOG_LEVEL, TERRAFORM_ANSIBLE_GROUPS,
                         TERRAFORM_ANSIBLE_INVENTORY, TERRAFORM_DATA_TYPES,
                         TERRAFORM_INVENTORY, TERRAFORM_LOAD_BALANCERS)
