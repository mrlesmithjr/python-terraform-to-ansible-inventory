import consul
import json
from .. logging_config import setup as LoggingConfigSetup


def load(ARGS, LOG_LEVEL):
    """Collect Consul backend data."""
    LOGGER = LoggingConfigSetup(LOG_LEVEL)
    CONSUL_HOST = ARGS.consulHost
    CONSUL_KV_PAIR = ARGS.consulKV
    CONSUL_PORT = ARGS.consulPort
    CONSUL_SCHEME = ARGS.consulScheme
    LOGGER.info('Loading data from %s://%s:%s/v1/kv/%s' %
                (CONSUL_SCHEME, CONSUL_HOST, CONSUL_PORT, CONSUL_KV_PAIR))
    CONSUL = consul.Consul(
        host=CONSUL_HOST, port=CONSUL_PORT, scheme=CONSUL_SCHEME)

    KEY, VALUE = CONSUL.kv.get(CONSUL_KV_PAIR, recurse=False)
    DATA_VALUE = VALUE['Value']
    DATA = json.loads(DATA_VALUE)
    LOGGER.debug(DATA)

    return DATA
