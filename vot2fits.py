"""
convert vot to fits format file

"""

import os
import sys
import time

import numpy as np

t0 = time.time()
import astropy
print('Elapsed time(secs):', time.time() - t0)
print()
print(astropy.__version__)

from astropy.table import Table
from astropy.io.votable import from_table, writeto

# import private functions
# sys.path.append("/home/rgm/soft/python/lib/")
from .fix_votable_object import fix_votable_object

def getargs(verbose=False):
    """

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
    parser =  argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    # the destination defaults to the option parameter
    # defaul=False might not be needed

    parser.add_argument("--infile",
                        help="Input file name")

    parser.add_argument("--info",
                        action='store_true',
                        help="table info")

    parser.add_argument("--stats",
                        action='store_true',
                        help="table statistics")

    parser.add_argument("--fixvot",
                        action='store_true',
                        help="fix vot object problem")

    parser.add_argument("--debug",
                        action='store_true',
                        help="debug option")

    parser.add_argument("--verbose", default=verbose,
                        action='store_true',
                        help="verbose option")

    parser.add_argument("--version", action='store_true',
                        help="verbose option")


    args = parser.parse_args()


    if args.debug or args.verbose:
        print('Number of arguments:', len(sys.argv),
              'arguments: ', sys.argv[0])

    if args.debug or args.verbose:
        pprint.pprint(args)

    if args.version:
        print('version:', __version__)
        sys.exit(0)


    return args



if __name__=='__main__':

    args = getargs()

    fixvot = args.fixvot

    infile = args.infile

    print('Reading:', infile)
    table = Table.read(infile)

    if args.info:
        table.info()

    if args.stats:
        table.info('stats')

    if fixvot:
        table = fix_votable_object(table)

    # filename without file extension
    infile_basename = os.path.splitext(os.path.basename(infile))[0]
    infile_extension = os.path.splitext(os.path.basename(infile))[1]

    print(os.path.splitext(os.path.basename(infile))[0])
    print(os.path.splitext(os.path.basename(infile))[1])

    outfile = 'tmp.fits'
    outfile = infile_basename + '.fits'

    print('Write:', outfile)
    table.write(outfile)
