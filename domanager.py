#!/usr/bin/env python

import argparse
import sys

from configuration import Configuration
from create import create
from destroy import destroy


def do_create(args):
    """Create a droplet based on configuration"""
    config = Configuration()
    config.read_config(args.config_file)
    create(config)


def do_destroy(args):
    """Destroy a droplet based on configuration"""
    config = Configuration()
    config.read_config(args.config_file)
    destroy(config)


def main(args):
    """Parse arguments and call create/destroy function"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')

    parser_create = subparsers.add_parser('create')
    parser_create.set_defaults(func=do_create)
    parser_create.add_argument('config_file',
                               help='Configuration file to use')

    parser_destroy = subparsers.add_parser('destroy')
    parser_destroy.set_defaults(func=do_destroy)
    parser_destroy.add_argument('config_file',
                                help='Configuration file to use')

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main(sys.argv)