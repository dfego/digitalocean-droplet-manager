#!/usr/bin/env python

import argparse
import digitalocean
import helper
import sys

from configuration import Configuration


def _update_domain(manager, domain_name, ip_address):
    """Update a domain entry with a new A record IP address"""
    domains = manager.get_all_domains()
    for domain in domains:
        if domain.name == domain_name:
            record = domain.create_new_domain_record(type='A', name='@',
                                                     data=ip_address)

def create(config):
    """Create a droplet based on the configuration given"""

    # Create manager
    manager = digitalocean.Manager(token=config.token)

    # Don't continue if we've already got droplet created
    if helper.get_droplet_by_name(manager, config.droplet_name):
        print 'Droplet already exists: {}'.format(config.droplet_name)
        return False

    # Get image to create droplet from
    image = helper.get_image_by_name(manager, config.image_name)

    # Fetch the ssh key
    ssh_keys = helper.get_ssh_keylist_by_name(manager, config.ssh_key_name)

    # Create droplet with image and ssh key
    droplet = digitalocean.Droplet(token=config.token,
                                   name=config.droplet_name,
                                   region=config.droplet_region,
                                   image=image.id,
                                   size_slug=config.droplet_size_slug,
                                   ssh_keys=ssh_keys)
    droplet.create()

    # Only expecting to see a single action, but loop anyway...
    actions = droplet.get_actions()
    for action in actions:
        action.wait()
        print 'Action {} is {}'.format(action.type, action.status)

    # Now get the IP address
    droplet.load()
    print 'IP address: {}'.format(droplet.ip_address)

    # Now get and upate the DNS record -- assumes a single A record
    # TODO create domain if it doesn't exist and move this to a function
    _update_domain(manager, config.domain_name, droplet.ip_address)

    print 'Setup of {} complete! IP address: {}'.format(config.domain_name,
                                                        droplet.ip_address)


if __name__ == '__main__':
    # Use argparse, even though just getting on arg for now
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='configuration file to use')
    args = parser.parse_args()

    # Read config file
    config = Configuration()
    if not config.read_config(args.config_file):
        sys.exit(1)

    create(config)
