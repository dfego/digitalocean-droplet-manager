#!/usr/bin/env python

import ConfigParser


class Configuration:
    def __init__(self):
        self.token = None
        self.droplet_name = None
        self.droplet_region = None
        self.droplet_size_slug = None
        self.image_name = None
        self.domain_name = None
        self.ssh_key_name = None

    def read_config(self, config_file):
        """Return configuration object"""
        config = ConfigParser.SafeConfigParser()
        files_read = config.read(config_file)
        if not files_read:
            return None

        # We have a config, now read it
        # TODO error handling if missing configs
        self.token = config.get('misc', 'token')
        self.droplet_name = config.get('droplet', 'name')
        self.droplet_region = config.get('droplet', 'region')
        self.droplet_size_slug = config.get('droplet', 'size_slug')
        self.image_name = config.get('droplet', 'image_name')
        self.domain_name = config.get('domain', 'name')
        self.ssh_key_name = config.get('ssh', 'key_name')
