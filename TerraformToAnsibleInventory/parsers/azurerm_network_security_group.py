from .. logging_config import setup as LoggingConfigSetup


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_SECURITY_GROUPS):
    """Populate Azure network security group info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    SECURITY_RULES = []
    SECURITY_GROUP = dict()

    for KEY, VALUE in raw_attrs.items():
        if 'security_rule' in KEY and '#' not in KEY:
            security_rule(raw_attrs, KEY, SECURITY_RULES)

    populate(raw_attrs, SECURITY_GROUP,
             SECURITY_RULES, TERRAFORM_SECURITY_GROUPS)


def security_rule(raw_attrs, KEY, SECURITY_RULES):
    """Populate Azure security rules."""
    SECURITY_RULE = dict()
    RULE_ID = KEY.split('.')[1]
    RULE_ACCESS = ('security_rule.%s.access' % RULE_ID)
    RULE_DESCRIPTION = ('security_rule.%s.description' % RULE_ID)
    RULE_DESTINATION_ADDRESS_PREFIX = (
        'security_rule.%s.destination_address_prefix' % RULE_ID)
    RULE_DESTINATION_PORT_RANGE = (
        'security_rule.%s.destination_port_range' % RULE_ID)
    RULE_DIRECTION = ('security_rule.%s.direction' % RULE_ID)
    RULE_NAME = ('security_rule.%s.name' % RULE_ID)
    RULE_PRIORITY = ('security_rule.%s.priority' % RULE_ID)
    RULE_PROTOCOL = ('security_rule.%s.protocol' % RULE_ID)
    RULE_SOURCE_ADDRESS_PREFIX = (
        'security_rule.%s.source_address_prefix' % RULE_ID)
    RULE_SOURCE_PORT_RANGE = (
        'security_rule.%s.source_port_range' % RULE_ID)

    SECURITY_RULE.update(
        {
            'access': raw_attrs[RULE_ACCESS],
            'description': raw_attrs[RULE_DESCRIPTION],
            'destination_address_prefix':
            raw_attrs[RULE_DESTINATION_ADDRESS_PREFIX],
            'destination_port_range':
            raw_attrs[RULE_DESTINATION_PORT_RANGE],
            'direction': raw_attrs[RULE_DIRECTION],
            'name': raw_attrs[RULE_NAME],
            'priority': raw_attrs[RULE_PRIORITY],
            'protocol': raw_attrs[RULE_PROTOCOL],
            'source_address_prefix':
            raw_attrs[RULE_SOURCE_ADDRESS_PREFIX],
            'source_port_range': raw_attrs[RULE_SOURCE_PORT_RANGE]
        }
    )

    if SECURITY_RULE not in SECURITY_RULES:
        SECURITY_RULES.append(SECURITY_RULE)


def populate(raw_attrs, SECURITY_GROUP, SECURITY_RULES,
             TERRAFORM_SECURITY_GROUPS):
    """Populate Azure security groups."""
    SECURITY_GROUP.update(
        {
            'id': raw_attrs['id'],
            'name': raw_attrs['name'],
            'location': raw_attrs['location'],
            'resource_group_name': raw_attrs['resource_group_name'],
            'security_groups': [
                {
                    'name': raw_attrs['name'],
                    'rules': SECURITY_RULES
                }
            ]
        }
    )

    if SECURITY_GROUP not in TERRAFORM_SECURITY_GROUPS:
        TERRAFORM_SECURITY_GROUPS.append(SECURITY_GROUP)
