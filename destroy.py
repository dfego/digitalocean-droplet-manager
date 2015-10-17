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
    droplet_size_slug = config.get('droplet', 'size_slug')
    domain_name = config.get('domain', 'name')

    # Create manager
    manager = digitalocean.Manager(token=token)

    # Get droplet so we can destroy it
    droplet = get_droplet_by_name(droplet_name)
    if droplet:
        print 'Droplet exists: {}'.format(droplet_name)
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
        if domain.name == domain_name:
            records = domain.get_records()
            for record in records:
                if record.type == 'A':
                    record.destroy()

    print 'Destroy of {} complete!'.format(domain_name)
