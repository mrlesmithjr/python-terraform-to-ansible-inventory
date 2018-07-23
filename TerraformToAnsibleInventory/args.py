import argparse
from _version import __version__


def parse():
    """Parse command line arguments."""
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-b', '--backend',
                        help='Define which Terraform backend to parse',
                        choices=['local', 'consul'], default='local')
    PARSER.add_argument('-cH', '--consulHost',
                        help='Define Consul host when using Consul backend')
    PARSER.add_argument('-cKV', '--consulKV',
                        help='Define Consul KV Pair to query. Ex. Azure/Test')
    PARSER.add_argument('-cP', '--consulPort',
                        help='Define Consul host port', default='8500')
    PARSER.add_argument('-cS', '--consulScheme',
                        help='Define Consul connection scheme.',
                        choices=['http', 'https'], default='http')
    PARSER.add_argument('-i', '--inventory', help='Ansible inventory',
                        default='./terraform_inventory.yml')
    PARSER.add_argument('--logLevel', help='Define logging level output',
                        choices=['CRITICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'], default='INFO')
    PARSER.add_argument('-t', '--tfstate', help='Terraform tftstate file',
                        default='./terraform.tfstate')
    PARSER.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    ARGS = PARSER.parse_args()
    if ARGS.backend == 'consul' and ARGS.consulHost is None:
        PARSER.error('Consul host is required when using Consul backend.')
    if ARGS.backend == 'consul' and ARGS.consulKV is None:
        PARSER.error('Consul KV pair is required when using Consul backend')
    return ARGS
