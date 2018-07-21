import json


def load(TERRAFORM_TFSTATE):
    with open(TERRAFORM_TFSTATE) as json_file:
        DATA = json.load(json_file)

    return DATA
