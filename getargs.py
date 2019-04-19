def getargs(verbose=False):
    """

    Template getargs function

    Usage

    python getargs.py --help


    def getargs():

    ....

    if __name__=='__main__':

        args = getargs()
        debug = args.debug()



    parse command line arguements

    not all args are active

    """
    import sys
    import pprint
    import argparse

    # there is probably a version function out there
    __version__ = '0.1'

    description = 'This is a template using getargs'
    epilog = """WARNING: Not all options may be supported
             """
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # the destination defaults to the option parameter
    # defaul=False might not be needed

    # default type is string
    parser.add_argument("--string",
                        help="string input")

    parser.add_argument("--float", type=float,
                        help="float input")

    parser.add_argument("--configfile",
                        default=None,
                        help="configuration file")

    parser.add_argument("--infile",
                        help="Input file name")

    parser.add_argument("--debug",
                        action='store_true',
                        help="debug option")

    parser.add_argument("--pause",
                        action='store_true',
                        help="Pausing option")

    parser.add_argument("--verbose", default=verbose,
                        action='store_true',
                        help="Verbose option")

    parser.add_argument("--Version", action='store_true',
                        help="verbose option")

    args = parser.parse_args()

    if args.debug or args.verbose:
        print()
        print('Number of arguments:', len(sys.argv),
              'arguments: ', sys.argv[0])

    if args.debug or args.verbose:
        print()
        for arg in vars(args):
            print(arg, getattr(args, arg))

    if args.debug or args.verbose:
        print()
        pprint.pprint(args)

    if args.version:
        print('version:', __version__)
        sys.exit(0)

    return args


if __name__ == '__main__':

    args = getargs(verbose=True)
