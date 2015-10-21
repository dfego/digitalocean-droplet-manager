#!/usr/bin/env python

import argparse
import digitalocean
import helper
import sys

from configuration import Configuration


def destroy(config):
    """Destroy a droplet based on the configuration given"""
    # Create manager
    manager = digitalocean.Manager(token=config.token)

    # Get droplet so we can destroy it
    droplet = helper.get_droplet_by_name(manager, config.droplet_name)
    if not droplet:
        print 'Droplet does not exist: {}'.format(config.droplet_name)
        return False

    droplet.destroy()

    # Should probably only see one?
    actions = droplet.get_actions()
    for action in actions:
        action.wait()
        print 'Action {} is {}'.format(action.type, action.status)

    # Now get and upate the DNS record -- assumes a single A record, which we
    # delete
    domains = manager.get_all_domains()
    for domain in domains:
        if domain.name == config.domain_name:
            records = domain.get_records()
            for record in records:
                if record.type == 'A':
                    record.destroy()

    print 'Destroy of {} complete!'.format(config.domain_name)
    return True


if __name__ == '__main__':
    # Use argparse, even though just getting on arg for now
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='configuration file to use')
    args = parser.parse_args()

    # Read config file
    config = Configuration()
    if not config.read_config(args.config_file):
        sys.exit(1)

    destroy(config)
