"""


"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# raw_input is replaced by input in Python 3
from builtins import input
try:
   input = raw_input
except NameError:
   pass

# The ConfigParser module has been renamed to configparser in Python 3
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

def rd_config_wsdb(configfile='wsdb.cfg', table=None, silent=False):
    """

    read WSDB config file

    """
    import configparser
    config = configparser.RawConfigParser()
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
            configfile = os.path.join(os.environ["HOME"], "wsdb.ini")
            print('trying ', configfile)
            config.read(configfile)

        host = config.get('wsdb', 'host')
        db = config.get('wsdb', 'db')
        user = config.get('wsdb', 'user')
        password = config.get('wsdb', 'password')
        if table is not None:
            table = config.get('wsdb', table)

    except Exception as e:
        print('Problem reading config file for wsdb: ', configfile)
        print(e)

    return db, host, user, password, table
