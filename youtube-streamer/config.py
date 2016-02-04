#!/usr/bin/env python3

import os
import os.path
import subprocess
import sys
import yaml

CONFIG_FILENAME = 'credentials'

creds = {"YOUTUBE_URL": "", "YOUTUBE_KEY": ""}


def set_config(config_file, config_yaml):
    """save config in a shell sourceable config_file"""
    global creds
    with open(config_file, 'w') as f:
        try:
            creds = config_yaml['config'][os.environ['SNAP_NAME']]
        except (KeyError, TypeError):
            default = {'config': {
                          os.environ['SNAP_NAME']: creds } }
            print("You need to give a yaml file like: {}".format(default))
        save_shell_source(f, creds)


def save_shell_source(config_fd, creds):
    """Save in fd from creds dict"""
    for (key, value) in creds.items():
        config_fd.write("{}={}\n".format(key, value))
            

if __name__ == '__main__':
    config_file = os.path.join(os.environ['SNAP_APP_DATA_PATH'], CONFIG_FILENAME)

    config_yaml = yaml.load(sys.stdin)
    if config_yaml:
        set_config(config_file, config_yaml)

    # try restarting the service
    subprocess.call(["snappy", "service", "restart", os.environ['SNAP_NAME'])

