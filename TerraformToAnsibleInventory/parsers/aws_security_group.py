from .. logging_config import setup as LoggingConfigSetup

EGRESS_RULES = []
INGRESS_RULES = []


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_SECURITY_GROUPS):
    """Populate AWS security group info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)
    SECURITY_RULES = []
    SECURITY_GROUP = dict()

    for KEY, VALUE in raw_attrs.items():
        if 'egress' in KEY and '#' not in KEY:
            egress(KEY, VALUE, raw_attrs)
        elif 'ingress' in KEY and '#' not in KEY:
            ingress(KEY, VALUE, raw_attrs)

    populate(raw_attrs, SECURITY_GROUP,
             SECURITY_RULES, TERRAFORM_SECURITY_GROUPS)


def egress(KEY, VALUE, raw_attrs):
    EGRESS_RULE = dict()
    EGRESS_CIDR_BLOCKS = []
    EGRESS_ID = KEY.split('.')[1]
    EGRESS_FROM_PORT = ('egress.%s.from_port' % EGRESS_ID)
    EGRESS_TO_PORT = ('egress.%s.to_port' % EGRESS_ID)
    EGRESS_TO_PROTOCOL = ('egress.%s.protocol' % EGRESS_ID)
    EGRESS_SELF = ('egress.%s.self' % EGRESS_ID)

    if ('egress.%s.cidr_blocks' % EGRESS_ID) in KEY and '#' not in KEY:
        if VALUE not in EGRESS_CIDR_BLOCKS:
            EGRESS_CIDR_BLOCKS.append(VALUE)

    EGRESS_RULE.update(
        {
            'cidr_blocks': EGRESS_CIDR_BLOCKS,
            'from_port': raw_attrs[EGRESS_FROM_PORT],
            'to_port': raw_attrs[EGRESS_TO_PORT],
            'protocol': raw_attrs[EGRESS_TO_PROTOCOL],
            'self': raw_attrs[EGRESS_SELF]
        }
    )

    if EGRESS_RULE not in EGRESS_RULES:
        EGRESS_RULES.append(EGRESS_RULE)


def ingress(KEY, VALUE, raw_attrs):
    INGRESS_RULE = dict()
    INGRESS_CIDR_BLOCKS = []
    INGRESS_ID = KEY.split('.')[1]
    INGRESS_FROM_PORT = ('ingress.%s.from_port' % INGRESS_ID)
    INGRESS_TO_PORT = ('ingress.%s.to_port' % INGRESS_ID)
    INGRESS_TO_PROTOCOL = ('ingress.%s.protocol' % INGRESS_ID)
    INGRESS_SELF = ('ingress.%s.self' % INGRESS_ID)

    if ('ingress.%s.cidr_blocks' % INGRESS_ID) in KEY and '#' not in KEY:
        if VALUE not in INGRESS_CIDR_BLOCKS:
            INGRESS_CIDR_BLOCKS.append(VALUE)

    INGRESS_RULE.update(
        {
            'cidr_blocks': INGRESS_CIDR_BLOCKS,
            'from_port': raw_attrs[INGRESS_FROM_PORT],
            'to_port': raw_attrs[INGRESS_TO_PORT],
            'protocol': raw_attrs[INGRESS_TO_PROTOCOL],
            'self': raw_attrs[INGRESS_SELF]
        }
    )

    if INGRESS_RULE not in INGRESS_RULES:
        INGRESS_RULES.append(INGRESS_RULE)


def populate(raw_attrs, SECURITY_GROUP, SECURITY_RULES,
             TERRAFORM_SECURITY_GROUPS):
    SECURITY_GROUP.update(
        {
            'description': raw_attrs['description'],
            'id': raw_attrs['id'],
            'name': raw_attrs['name'],
            'security_groups': [
                {
                    'id': raw_attrs['id'],
                    'name': raw_attrs['name'],
                    'description': raw_attrs['description'],
                    'egress_rules': EGRESS_RULES,
                    'ingress_rules': INGRESS_RULES
                }
            ]
        }
    )

    if SECURITY_GROUP not in TERRAFORM_SECURITY_GROUPS:
        TERRAFORM_SECURITY_GROUPS.append(SECURITY_GROUP)
