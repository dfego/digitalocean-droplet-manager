#!/usr/bin/env python

import argparse
import digitalocean
import sys
import ConfigParser

# Available droplets
def get_droplet_by_name(manager, name):
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        if droplet.name == name:
            return droplet

    return None

def get_image_by_name(manager, name):
    my_images = manager.get_my_images()
    for image in my_images:
        if image.name == name:
            return image

    return None

def get_ssh_keylist_by_name(manager, name):
    """ Return a size 0 or 1 ssh key list by name """
    all_ssh_keys = manager.get_all_sshkeys()
    ssh_keys = []
    for key in all_ssh_keys:
        if key.name == name:
            ssh_keys.append(key)

    return ssh_keys

if __name__ == '__main__':
    # Use argparse, even though just getting on arg for now
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='configuration file to use')
    args = parser.parse_args()

    # Read config file
    config = ConfigParser.SafeConfigParser()
    files_read = config.read(args.config_file)
    if not files_read:
        print 'Configuration file cannot be read. Exiting.'
        sys.exit(1)

    #  Parse out values
    token = config.get('misc', 'token')
    droplet_name = config.get('droplet', 'name')
    droplet_region = config.get('droplet', 'region')
    droplet_size_slug = config.get('droplet', 'size_slug')
    image_name = config.get('droplet', 'image_name')
    domain_name = config.get('domain', 'name')
    ssh_key_name = config.get('ssh', 'key_name')

    # Create manager
    manager = digitalocean.Manager(token=token)

    # Don't continue if we've already got droplet created
    if get_droplet_by_name(manager, droplet_name):
        print 'Droplet already exists: {}'.format(droplet_name)
        sys.exit(0) 

    # Get image to create droplet from
    image = get_image_by_name(manager, image_name)

    # Fetch the ssh key
    ssh_keys = get_ssh_keylist_by_name(manager, ssh_key_name)

    # Create droplet with image and ssh key
    droplet = digitalocean.Droplet(token=token,
            name=droplet_name,
            region=droplet_region,
            image=image.id,
            size_slug=droplet_size_slug,
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
    domains = manager.get_all_domains()
    for domain in domains:
        if domain.name == domain_name:
            record = domain.create_new_domain_record(type='A', name='@',
                    data=droplet.ip_address)

    print 'Setup of {} complete! IP address: {}'.format(domain_name, droplet.ip_address)
