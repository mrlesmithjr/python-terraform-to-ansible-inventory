import consul
import json
# import sys


def backend(ARGS):
    """Collect Consul backend data."""
    CONSUL_HOST = ARGS.consulHost
    CONSUL_KV_PAIR = ARGS.consulKV
    CONSUL_PORT = ARGS.consulPort
    CONSUL_SCHEME = ARGS.consulScheme
    CONSUL = consul.Consul(
        host=CONSUL_HOST, port=CONSUL_PORT, scheme=CONSUL_SCHEME)

    KEY, VALUE = CONSUL.kv.get(CONSUL_KV_PAIR, recurse=False)
    DATA_VALUE = VALUE['Value']
    DATA = json.loads(DATA_VALUE)

    return DATA
