#!/usr/bin/env python


def get_droplet_by_name(manager, name):
    """Returns a droplet for the given name, or None"""
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        if droplet.name == name:
            return droplet

    return None


def get_image_by_name(manager, name):
    """Returns the image object with the given name, or None if not found"""
    my_images = manager.get_my_images()
    for image in my_images:
        if image.name == name:
            return image

    return None


def get_ssh_keylist_by_name(manager, name):
    """Returns a keylist with the given named key, or empty if not found"""
    all_ssh_keys = manager.get_all_sshkeys()
    ssh_keys = []
    for key in all_ssh_keys:
        if key.name == name:
            ssh_keys.append(key)

    return ssh_keys
