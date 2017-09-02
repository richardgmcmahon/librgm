"""


"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

def rd_config(configfile=None, table=None, silent=False):
    """

    read config file

    look in cwd, home and home/.config

    home/.config not implemented yet


    """
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    # read database connection info from config file
    # could check if existence in some default locations rather
    # using try

    try:
        if not silent:
            print('Reading config file', configfile)

        try:
            config.read(configfile)
        except IOError:
            print('config file', configfile, "does not exist")
            configfile = os.path.join(os.environ["HOME"], configfile)
            print('trying ', configfile)
            config.read(configfile)

    except Exception as e:
        print('Problem reading config file: ', configfile)
        print(e)


    return configfile
