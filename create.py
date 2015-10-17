#!/usr/bin/env python

import digitalocean
import sys
import ConfigParser

# Available droplets
def get_droplet_by_name(name):
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        if droplet.name == name:
            return droplet

    return None

def get_image_by_name(name):
    my_images = manager.get_my_images()
    for image in my_images:
        if image.name == name:
            return image

    return None

if __name__ == '__main__':
    # Read config file
    config = ConfigParser.SafeConfigParser()
    config.read('do.cfg')

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
    if get_droplet_by_name(droplet_name):
        print 'Droplet already exists: {}'.format(droplet_name)
        sys.exit(0) 

    # Get image to create droplet from
    image = get_image_by_name(image_name)

    # For now, just get all SSH keys and copy them on
    all_ssh_keys = manager.get_all_sshkeys()
    ssh_keys = []
    for key in all_ssh_keys:
        if key.name == ssh_key_name:
            ssh_keys.append(key)

    # Create droplet with image and ssh key
    droplet = digitalocean.Droplet(token=token,
            name=droplet_name,
            region=droplet_region,
            image=image.id,
            size_slug=droplet_size_slug,
            ssh_keys=ssh_keys)
    droplet.create()

    # Should probably only see one?
    actions = droplet.get_actions()
    for action in actions:
        action.wait()
        print 'Action {} is {}'.format(action.type, action.status)

    # Now get the IP address...
    droplet.load()
    print 'IP address: {}'.format(droplet.ip_address)

    # Now get and upate the DNS record -- assumes a single A record
    domains = manager.get_all_domains()
    for domain in domains:
        if domain.name == domain_name:
            record = domain.create_new_domain_record(type='A', name='@',
                    data=droplet.ip_address)

    print 'Setup of {} complete! IP address: {}'.format(domain_name, droplet.ip_address)
