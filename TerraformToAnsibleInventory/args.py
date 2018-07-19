import argparse


def parse():
    """Parse command line arguments."""
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-i", "--inventory", help="Ansible inventory",
                        default='./terraform_inventory.yml')
    PARSER.add_argument("-t", "--tfstate", help="Terraform tftstate file",
                        default='./terraform.tfstate')
    ARGS = PARSER.parse_args()
    return ARGS
