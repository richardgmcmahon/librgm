def getconfig(configfile=None, debug=False, silent=False):
    """
    read config file

    Note the Python 2 ConfigParser module has been renamed to configparser
    in Python 3 so it better to use import configparser in Python 2 for
    future proofing

    see also getconfig.cfg

    TODO: catch exceptions

    Support for lists:

    see:

    https://stackoverflow.com/questions/335695/lists-in-configparser

    https://github.com/cacois/python-configparser-examples

    look in cwd, home and home/.config

    home/.config not implemented yet


    """
    import os
    import configparser

    # read the configuration file
    # config = configparser.RawConfigParser()
    config = configparser.SafeConfigParser()

    print('__file__', __file__)
    if configfile is None:
        if debug:
            print('__file__', __file__)
        configfile_default = os.path.splitext(__file__)[0] + '.cfg'
    if configfile is not None:
        configfile_default = configfile

    print('Open configfile:', configfile)
    if debug:
        print('Open configfile:', configfile)

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

    if debug:
        print('configfile:', configfile)
        print('sections:', config.sections())
        for section_name in config.sections():
            print('Section:', section_name)
            print('Options:', config.options(section_name))
            for name, value in config.items(section_name):
                print('  %s = %s' % (name, value))

        print()
        print()

        for section_name in config.sections():
            print()
            print('Section:', section_name)
            for name, value in config.items(section_name):
                print('  %s = %s' % (name, value))
                print(section_name, ':',
                      name, config.get(section_name, name))

    return config


if __name__ == '__main__':

    configfile = 'getconfig.cfg'
    config = getconfig(configfile=configfile, debug=True)
