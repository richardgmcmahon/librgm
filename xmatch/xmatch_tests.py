"""

astropy based table version

could also use Sergey Koposov's version based on scipy kd-tree

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys
import time


# standard library fucntions
import numpy as np
import matplotlib.pyplot as plt

# 3rd party functions
from astropy.table import Table, Column
from astropy.coordinates import FK4, FK5
from astropy.coordinates import Angle
from astropy.stats import mad_std

# private functions
sys.path.append("/home/rgm/soft/python/lib/")
from librgm.plotid import plotid
from librgm.plot_radec import plot_radec
from librgm.xmatch import xmatch_cat
from librgm.xmatch import xmatch_checkplot
from librgm.xmatch import xmatch_checkplots
from librgm.xmatch import xmatch_selfcheck


def mk_data(ndata=10000, savefig=True,
            rarange=None, decrange=None,
            astrotable=True,
            plots=True,
            projection=None):
    """

    dtypes default to int64 and float64 which could be inefficient
    TODO:
    investigate use of int32 and float32 for reducing memory needs
    and processing speed as a fucntion of dataset size.

    """
    ndata =  int(ndata)
    ra = np.random.uniform(0.0, 360.0, ndata)
    cosdec = np.random.uniform(-1.0, 1.0, ndata)
    dec = np.rad2deg(np.arccos(cosdec)) - 90.0

    if plots:
        plt.figure(figsize=(8,7))

        # aitiff, hammer, mollweide
        # projection = 'aitoff'
        # projection = 'hammer'
        # projection = 'mollweide'
        if projection is not None:
            plt.subplot(2, 1, 1, projection=projection)
        if projection is None:
            plt.subplot(2, 1, 1)

        xdata = ra
        ydata = dec
        xrange = [np.min(xdata), np.max(xdata)]
        yrange = [np.min(ydata), np.max(ydata)]

        ndata = len(xdata)
        plt.plot(xdata, ydata, '.',
                 ms=0.5, alpha=0.5,
                 label=str(ndata))

        if projection is None:
            plt.xlim(xrange)
            plt.ylim(yrange)

        if projection is None:
            projection = ''

        plt.suptitle('suptitle: xmatch regression tests')
        plt.title('title:' + projection)

        plt.xlabel('RA(degree)')
        plt.ylabel('Dec(degree)')

        plt.grid()
        plt.legend(loc='upper right')


        # 2nd plot
        plt.subplot(2, 1, 2)
        ydata = cosdec
        ndata = len(xdata)
        plt.plot(xdata, ydata, '.', ms=0.5, alpha=0.5, label=str(ndata))

        xrange = [np.min(xdata), np.max(xdata)]
        yrange = [np.min(ydata), np.max(ydata)]

        plt.title('title: xmatch regression tests')
        plt.xlabel('RA(degree)')
        plt.ylabel('Cosine(Dec)')

        plt.legend(loc='upper right')

        plt.xlim(xrange)
        plt.ylim(yrange)

        plt.grid()

        plotid()


        if savefig:
            plotfile = 'xmatch_tests_radec.png'
            print('Saving:', plotfile)
            plt.savefig(plotfile)

        plt.show()

    nrows = len(ra)
    print('Number of rows:', nrows)

    # create astropy table
    if astrotable:
        result = Table()
        result['id'] = Column(np.linspace(1, nrows, num=nrows, dtype=int),
                              description=['ID'])
        result['ra'] = Column(ra, unit='deg',
                             description=['Right Ascension'])
        result['dec'] = Column(dec, unit='deg',
                             description=['Declination'])

        result.info()
        result.info('stats')

    return result


def getargs():
    """

    """

    import argparse

    t0 = time.time()

    __version__ = '0.1'

    description = 'xmatch tests'
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=description)

    n1_default = int(1e4)
    parser.set_defaults(n1=n1_default)
    parser.add_argument("--n1", type=int,
                        help="Number of data points in table 1")

    parser.add_argument("--n2", type=int, default=0,
                        help="Number of data points in table 2")

    parser.add_argument(
        "--rarange", default=[0.0, 360.0], type=float, nargs=2,
        help="RA range in hours in form Deg Deg")

    parser.add_argument(
        "--decrange", default=[-90.0, 30.0], type=float, nargs=2,
        help="Declination range in degrees in form Deg Deg")

    parser.add_argument("--projection", action="store_true",
                        help="optional verbose mode")

    parser.add_argument("--verbose", action="store_true",
                        help="optional matplotlib projection")

    parser.add_argument("--debug", action="store_true",
                        dest='debug',
                        help="optional debug very verbose mode")

    parser.add_argument("--pause", action="store_true",
                        dest='pause', help="turn on pausing option")

    parser.add_argument("-v", "--version", action="store_true",
                        dest="version",
                        default="", help="print version number and  exit")

    print('Number of arguments:', len(sys.argv), 'arguments: ', sys.argv[0])
    args = parser.parse_args()

    if args.version:
        print('version:', __version__)
        sys.exit(0)

    return args


if __name__ == '__main__':
    """


    """

    sys.path.append("/home/rgm/soft/python/lib/")
    from librgm import xmatch

    t0 = time.time()

    args = getargs()

    debug = args.debug

    if args.verbose or args.debug:
            help(xmatch)
    if args.debug:
        print('__file__:', __file__)
        help(xmatch_cat)

    multimatch = True
    savefig = True

    ndata1 = args.n1
    ndata2 = args.n2
    if ndata2 == 0:
        ndata2 = ndata1

    table1 = mk_data(ndata=ndata1, savefig=True)
    table2 = mk_data(ndata=ndata2, savefig=True, plots=False)
    print('Input data created:', len(table1), len(table2))
    print("Elapsed time %.3f seconds" % (time.time() - t0))

    """RA, Dec nearest xmatch for two lists; returns pointers """
    print('table1 selfxmatch')
    t0 = time.time()
    idxmatch, dr = xmatch_cat(table1=table1,
                              selfmatch=True,
                              stats=True,
                              debug=False,
                              verbose=True)
    print("Elapsed time %.3f seconds" % (time.time() - t0))
    if args.debug:
        raw_input('Type any key to continue> ')
    dr_median = np.median(dr)
    dr_mad_std = mad_std(dr)
    numpoints = len(dr)


    """Default is taken from the rcParam hist.bins."""
    prefix = os.path.basename(__file__)
    plt.suptitle(prefix + ': ' + 'dr histogram')
    plot_label = ("median:  {:.2f} arcsec".format(dr_median) + '\n' +
                  "mad_std: {:.2f} arcsec".format(dr_mad_std) + '\n' +
                  "npts: {}".format(numpoints))
    plt.hist(dr, bins=100, fill=False, histtype='step',
             label=plot_label)
    plt.grid()
    plt.xlabel('Pairwise radial separation (arcsec)')
    plt.ylabel('Frequency per bin')
    plt.legend()

    if savefig:
        plotfile = prefix + '_dr.png'
        print('Saving:', plotfile)
        plt.savefig(plotfile)

    plt.show()

    print("Elapsed time %.3f seconds" % (time.time() - t0))
    print("Elapsed time {:.3f} sec".format(time.time() - t0))

    if args.debug:
        raw_input('Type any key to continue> ')

    table = table1
    if args.debug:
        help(xmatch_selfcheck)

    table.info()
    table.info('stats')
    rmax = 7200.0
    binsize = 60.0
    idx = xmatch_selfcheck(data=table, rmax=rmax, binsize=binsize,
                           showplot=True, debug=debug)


    # xmatch table1 and table2
    table1.info()
    table1.info('stats')
    table2.info()
    table2.info('stats')

    print()
    print('xmatch table1 to table2:', len(table1), len(table2))
    t0 = time.time()
    if not multimatch:
        idxmatch, dr = xmatch_cat(table1=table1, table2=table2,
                                  stats=True,
                                  multimatch=False)
    if multimatch:
        idxmatch, dr = xmatch_cat(table1=table1, table2=table2,
                                  stats=True,
                                  seplimit=100.0,
                                  multimatch=True)
    print("Elapsed time %.3f seconds" % (time.time() - t0))

    t0 = time.time()
    print('method=True')
    idxmatch, dr = xmatch_cat(table1=table1, table2=table2,
                              stats=True,
                              method=True)
    print("Elapsed time %.3f seconds" % (time.time() - t0))

    # xmatch table2 and table1
    print()
    print('xmatch table2 to table1')
    t0 = time.time()
    idxmatch, dr = xmatch_cat(table1=table2, table2=table1)
    print("Elapsed time %.3f seconds" % (time.time() - t0))

    t0 = time.time()
    idxmatch, dr = xmatch_cat(table1=table2, table2=table1,
                              method=True)
    print("Elapsed time %.3f seconds" % (time.time() - t0))