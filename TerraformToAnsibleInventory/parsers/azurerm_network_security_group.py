import json
import yaml


def parse(RESOURCE, TERRAFORM_NETWORK_SECURITY_GROUPS):
    """Populate Azure network security group info."""
    raw_attrs = RESOURCE['primary']['attributes']
    SECURITY_RULE_IDS = dict()

    for KEY, VALUE in raw_attrs.items():
        if 'security_rule' in KEY and '#' not in KEY:
            RULE = KEY.split('.')
            RULE_ID = RULE[1]
            RULE_TYPE = RULE[2]
            if RULE_ID not in SECURITY_RULE_IDS:
                SECURITY_RULE_IDS.update({RULE_ID: dict()})
            SECURITY_RULE_IDS[RULE_ID].update({RULE_TYPE: VALUE})

    NETWORK_SECURITY_GROUP = dict()
    NETWORK_SECURITY_GROUP.update(
        {'id': raw_attrs['id'],
         'name': raw_attrs['name'],
         'location': raw_attrs['location'],
         'resource_group_name': raw_attrs['resource_group_name'],
         'security_group_rules': SECURITY_RULE_IDS})
    TERRAFORM_NETWORK_SECURITY_GROUPS.append(NETWORK_SECURITY_GROUP)
