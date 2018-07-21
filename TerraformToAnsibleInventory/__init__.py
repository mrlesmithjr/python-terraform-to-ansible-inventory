import os
from . args import parse as ArgsParse
from . parse import terraform_tfstate as ParseTerraformTfstate
from . build_inventory import terraform as BuildTerraformInventory
from . generate_inventory import ansible as GenerateAnsibleInventory

ARGS = ArgsParse()

CWD = os.getcwd()
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TERRAFORM_ANSIBLE_GROUPS = []
TERRAFORM_ANSIBLE_INVENTORY = ('%s/' + ARGS.inventory) % CWD
TERRAFORM_DATA_TYPES = []
TERRAFORM_INVENTORY = []
TERRAFORM_LOAD_BALANCERS = []
TERRAFORM_NETWORK_INTERFACES = []
TERRAFORM_NETWORK_SECURITY_GROUPS = []
TERRAFORM_PUBLIC_IPS = []
TERRAFORM_TFSTATE = ('%s/' + ARGS.tfstate) % CWD
TERRAFORM_VMS = []

ParseTerraformTfstate(ARGS, TERRAFORM_ANSIBLE_GROUPS,
                      TERRAFORM_NETWORK_INTERFACES,
                      TERRAFORM_LOAD_BALANCERS,
                      TERRAFORM_PUBLIC_IPS,
                      TERRAFORM_TFSTATE,
                      TERRAFORM_VMS, TERRAFORM_NETWORK_SECURITY_GROUPS)

BuildTerraformInventory(TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY,
                        TERRAFORM_NETWORK_INTERFACES,
                        TERRAFORM_PUBLIC_IPS, TERRAFORM_VMS,
                        TERRAFORM_NETWORK_SECURITY_GROUPS)

GenerateAnsibleInventory(
    TERRAFORM_ANSIBLE_GROUPS, TERRAFORM_ANSIBLE_INVENTORY,
    TERRAFORM_DATA_TYPES, TERRAFORM_INVENTORY, TERRAFORM_LOAD_BALANCERS)
