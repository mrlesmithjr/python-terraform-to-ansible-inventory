from .. logging_config import setup as LoggingConfigSetup

ACCESS_LOGS = []
AVAILABILITY_ZONES = []
HEALTH_CHECKS = []
INSTANCES = []
LISTENERS = []
LOAD_BALANCER = dict()
SECURITY_GROUPS = []
SUBNETS = []
TAGS = dict()


def parse(LOG_LEVEL, RESOURCE, TERRAFORM_LOAD_BALANCERS,
          TERRAFORM_PUBLIC_IPS):
    """Populate AWS ELB info."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    raw_attrs = RESOURCE['primary']['attributes']
    LOGGER.debug(raw_attrs)

    for KEY, VALUE in raw_attrs.items():
        if 'access_logs' in KEY and '#' not in KEY:
            access_logs(KEY, raw_attrs, ACCESS_LOGS)

        elif 'availability_zones' in KEY and '#' not in KEY:
            availability_zones(VALUE)

        elif 'health_check' in KEY and '#' not in KEY:
            health_checks(KEY, raw_attrs, HEALTH_CHECKS)

        elif 'instances' in KEY and '#' not in KEY:
            instances(VALUE)

        elif 'listener' in KEY and '#' not in KEY:
            listeners(KEY, raw_attrs, LISTENERS)

        elif 'security_groups' in KEY and '#' not in KEY:
            security_groups(VALUE)

        elif 'subnets' in KEY and '#' not in KEY:
            subnets(VALUE)

        elif 'tags' in KEY and '%' not in KEY:
            tags(KEY, VALUE)

    populate(raw_attrs, RESOURCE, TERRAFORM_LOAD_BALANCERS, LOGGER)


def access_logs(KEY, raw_attrs, ACCESS_LOGS):
    """Captures any access logs associated with the ELB."""
    ACCESS_LOG = dict()
    ACCESS_LOG_ID = KEY.split('.')[1]
    ACCESS_LOG_BUCKET = ('access_logs.%s.bucket' % ACCESS_LOG_ID)
    ACCESS_LOG_BUCKET_PREFIX = (
        'access_logs.%s.bucket_prefix' % ACCESS_LOG_ID)
    ACCESS_LOG_INTERVAL = ('access_logs.%s.interval' % ACCESS_LOG_ID)
    ACCESS_LOG.update(
        {
            'bucket': raw_attrs[ACCESS_LOG_BUCKET],
            'bucket_prefix': raw_attrs[ACCESS_LOG_BUCKET_PREFIX],
            'interval': raw_attrs[ACCESS_LOG_INTERVAL]
        }
    )
    if ACCESS_LOG not in ACCESS_LOGS:
        ACCESS_LOGS.append(ACCESS_LOG)


def availability_zones(VALUE):
    """Captures any availability zones associated with the ELB."""
    if VALUE not in AVAILABILITY_ZONES:
        AVAILABILITY_ZONES.append(VALUE)


def health_checks(KEY, raw_attrs, HEALTH_CHECKS):
    """Captures any health checks associated with the ELB."""
    HEALTH_CHECK = dict()
    HEALTH_CHECK_ID = KEY.split('.')[1]
    HEALTH_CHECK_HEALTHY_THRESHOLD = (
        'health_check.%s.healthy_threshold' % HEALTH_CHECK_ID)
    HEALTH_CHECK_UNHEALTHY_THRESHOLD = (
        'health_check.%s.unhealthy_threshold' % HEALTH_CHECK_ID)
    HEALTH_CHECK_TIMEOUT = (
        'health_check.%s.timeout' % HEALTH_CHECK_ID)
    HEALTH_CHECK_INTERVAL = (
        'health_check.%s.interval' % HEALTH_CHECK_ID)
    HEALTH_CHECK_TARGET = ('health_check.%s.target' % HEALTH_CHECK_ID)
    HEALTH_CHECK.update(
        {
            'healthy_threshold':
            raw_attrs[HEALTH_CHECK_HEALTHY_THRESHOLD],
            'unhealthy_threshold':
            raw_attrs[HEALTH_CHECK_UNHEALTHY_THRESHOLD],
            'timeout': raw_attrs[HEALTH_CHECK_TIMEOUT],
            'interval': raw_attrs[HEALTH_CHECK_INTERVAL],
            'target': raw_attrs[HEALTH_CHECK_TARGET]
        }
    )
    if HEALTH_CHECK not in HEALTH_CHECKS:
        HEALTH_CHECKS.append(HEALTH_CHECK)


def instances(VALUE):
    """Captures any instances associated with the ELB."""
    if VALUE not in INSTANCES:
        INSTANCES.append(VALUE)


def listeners(KEY, raw_attrs, LISTENERS):
    """Captures any listeners associated with the ELB."""
    LISTENER = dict()
    LISTENER_ID = KEY.split('.')[1]
    LISTENER_INSTANCE_PORT = (
        'listener.%s.instance_port' % LISTENER_ID)
    LISTENER_INSTANCE_PROTOCOL = (
        'listener.%s.instance_protocol' % LISTENER_ID)
    LISTENER_LB_PORT = ('listener.%s.lb_port' % LISTENER_ID)
    LISTENER_LB_PROTOCOL = ('listener.%s.lb_protocol' % LISTENER_ID)
    LISTENER.update(
        {
            'instance_port': raw_attrs[LISTENER_INSTANCE_PORT],
            'instance_protocol': raw_attrs[LISTENER_INSTANCE_PROTOCOL],
            'lb_port': raw_attrs[LISTENER_LB_PORT],
            'lb_protocol': raw_attrs[LISTENER_LB_PROTOCOL]
        }
    )
    if LISTENER not in LISTENERS:
        LISTENERS.append(LISTENER)


def security_groups(VALUE):
    """Captures any security groups associated with the ELB."""
    if VALUE not in SECURITY_GROUPS:
        SECURITY_GROUPS.append(VALUE)


def subnets(VALUE):
    """Captures any subnets associated with the ELB."""
    if VALUE not in SUBNETS:
        SUBNETS.append(VALUE)


def tags(KEY, VALUE):
    """Captures any tags associated with the ELB."""
    TAG_NAME = KEY.split('.')[1]
    TAGS.update({TAG_NAME: VALUE})


def populate(raw_attrs, RESOURCE, TERRAFORM_LOAD_BALANCERS, LOGGER):
    """Populates ELB configuration based on captured details."""
    LOAD_BALANCER.update(
        {
            'name': raw_attrs['name'],
            'access_logs': ACCESS_LOGS,
            'connection_draining': raw_attrs['connection_draining'],
            'connection_draining_timeout':
            raw_attrs['connection_draining_timeout'],
            'cross_zone_load_balancing':
            raw_attrs['cross_zone_load_balancing'],
            'dns_name': raw_attrs['dns_name'], 'health_checks': HEALTH_CHECKS,
            'idle_timeout': raw_attrs['idle_timeout'],
            'internal': raw_attrs['internal'],
            'security_groups': SECURITY_GROUPS, 'subnets': SUBNETS,
            'type': RESOURCE['type'], 'availability_zones': AVAILABILITY_ZONES,
            'listeners': LISTENERS, 'tags': TAGS, 'instances': INSTANCES,
            'zone_id': raw_attrs['zone_id']
        }
    )
    if LOAD_BALANCER not in TERRAFORM_LOAD_BALANCERS:
        LOGGER.debug(LOAD_BALANCER)
        TERRAFORM_LOAD_BALANCERS.append(LOAD_BALANCER)
