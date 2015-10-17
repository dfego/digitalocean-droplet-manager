#!/usr/bin/env python

import digitalocean
import sys

DROPLET_NAME = 'Mumble'
DROPLET_REGION = 'nyc3'
DROPLET_SIZE = '512mb'
#IMAGE_NAME = r'Murmur w/ Dynamic DNS'
IMAGE_NAME = r'Murmur Installed and Configured'

DOMAIN='mumble.danfego.net'

# Available droplets
def list_droplets():
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        print droplet

def get_droplet_by_name(name):
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        if droplet.name == name:
            return droplet

    return None

def list_images():
    my_images = manager.get_my_images()
    for image in my_images:
        if image.name == IMAGE_NAME:
            print image

def get_image_by_name(name):
    my_images = manager.get_my_images()
    for image in my_images:
        if image.name == name:
            return image

    return None

if __name__ == '__main__':
    # Create manager
    manager = digitalocean.Manager(token=TOKEN)

    # TODO argparse
    # Workflow:
    # 1. If droplet exists, exit (for now)
    # 2. Get image
    # 3. Create droplet with image and ssh key
    # 4. Setup DNS?

    # Don't continue if we've already got droplet created
    if get_droplet_by_name(DROPLET_NAME):
        print 'Droplet exists: {}'.format(DROPLET_NAME)
        sys.exit(0) 

    # Get image
    image = get_image_by_name(IMAGE_NAME)
    print image.id

    # For now, just get all SSH keys
    ssh_keys = manager.get_all_sshkeys()

    # Create droplet with image and ssh key
    droplet = digitalocean.Droplet(token=TOKEN,
            name=DROPLET_NAME,
            region=DROPLET_REGION,
            image=image.id,
            size_slug=DROPLET_SIZE,
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
        if domain.name == DOMAIN:
            record = domain.create_new_domain_record(type='A', name='@',
                    data=droplet.ip_address)

    print 'Setup of {} complete! IP address: {}'.format(DOMAIN, droplet.ip_address)
