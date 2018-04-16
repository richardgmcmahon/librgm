from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import time

import numpy as np
from matplotlib import pyplot as plt

from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.coordinates import BarycentricTrueEcliptic
import astropy.units as units

from librgm.plotid import plotid
from librgm.lineno import lineno

def plot_radec(table=None,
               xcolname='ra',
               ycolname='dec',
               ra=None,
               dec=None,
               rarange=None,
               decrange=None,
               frame='equatorial',
               projection='cartesian',
               aspect=None,
               overplot=False,
               figsize=(8.0, 8.0),
               title=None,
               suptitle=None,
               xlabel=None,
               ylabel=None,
               plotlabel='',
               plotstyle=None,
               marker='o',
               markersize=0.5,
               color='b',
               markeredgecolor='b',
               alpha=1.0,
               linestyle=None,
               showplot=False,
               plotfile=None,
               plotfile_prefix=None,
               plotfile_suffix=None,
               noplotid=False,
               legend=True,
               plotdir='./',
               savefig=True,
               verbose=False,
               debug=False):
    """

    assumes units are degree

    subplot projections need angles to be in radians

    Supports ra, dec lists or astropy table

    http://docs.astropy.org/en/stable/coordinates/skycoord.html#example-1-plotting-random-data-in-aitoff-projection

    http://www.astropy.org/astropy-tutorials/plot-catalog.html

    from astropy.coordinates import SkyCoord
    from astropy.coordinates import ICRS, Galactic, FK4, FK5
    from astropy.coordinates import BarycentricTrueEcliptic
    from astropy import units

    skycoords = SkyCoord(ra=ra, dec=dec, units='deg')
    galactic = skycoords.galactic

    xdata = galactic.l.wrap_at(180*units.deg)
    ydata = galactic.b.wrap_at(180*units.deg)
    plot(xdata, ydata)

    skycoords_ecliptic = skycoords.transform_to(BarycentricTrueEcliptic)

    """

    import time

    t0 = time.time()
    print(frame, projection)
    #plt.setp(lines, edgecolors='None')

    print('overplot:', overplot)
    if not overplot:
        print(figsize)
        plt.figure(num=None, figsize=figsize)
        if projection != "cartesian":
            plt.subplot(111, projection=projection)

    if table is not None:
       ra = table[xcolname]
       dec = table[ycolname]

    if frame == 'equatorial':
        if projection == 'cartesian':
            xdata = ra
            ydata = dec

        # convert to radians and wrap around at 180degrees so 0 is
        # in middle and range is -180 to +180 degrees althougf input
        # is in radians.
        if projection != 'cartesian':
            skycoords = SkyCoord(ra=ra, dec=dec, unit='deg')
            xdata = skycoords.ra.wrap_at(180 * units.deg).radian
            ydata = skycoords.dec.radian

    if debug:
        print('coordination transformation complete')
        print('Elapsed time(secs): ',time.time() - t0, lineno())

    if frame != 'equatorial':
        skycoords = SkyCoord(ra=ra, dec=dec, unit='deg')

    if frame == 'galactic':
        galactic = skycoords.galactic
        if projection == 'cartesian':
           xdata = galactic.l.degree
           ydata = galactic.b.degree

        if projection != 'cartesian':
           xdata = galactic.l.wrap_at(180 * units.deg).radian
           ydata = galactic.b.radian

    # convert ra, dec to ecliptic
    if frame == 'ecliptic':
        skycoords_ecliptic = skycoords.transform_to(BarycentricTrueEcliptic)
        if projection == 'cartesian':
            xdata = skycoords_ecliptic.lon.degree
            ydata = skycoords_ecliptic.lat.degree

        if projection != 'cartesian':
            xdata = skycoords_ecliptic.lon.wrap_at(180 * units.deg).radian
            ydata = skycoords_ecliptic.lat.radian

    if debug:
        print('coordination transformation complete')
        print('Elapsed time(secs): ',time.time() - t0, lineno())

    if verbose or debug:
        print(type(xdata), type(ydata), len(xdata))
        print('RA range: ', np.min(xdata), np.max(xdata))
        print('Dec range: ', np.min(ydata), np.max(ydata))

    if debug:
        print('Elapsed time(secs): ',time.time() - t0, lineno())
        print('plotstyle:', plotstyle)
    ndata = len(xdata)
    print('Number of points:', ndata, type(xdata), type(ydata))
    print(xdata.size, xdata.shape)
    print(ydata.size, ydata.shape)

    if debug:
        print()
        print('plotstyle:', plotstyle)
        print('point plotting starting')
        print('Elapsed time(secs): ',time.time() - t0, lineno())

    if plotstyle is None:
        print(marker, markersize, alpha, color, markeredgecolor)
        plt.plot(xdata, ydata,
                 marker=marker, color=color,
                 markersize=markersize,
                 alpha=alpha,
                 markeredgecolor=markeredgecolor,
                 linestyle='None',
                 label=plotlabel + str(ndata))

    # this is placeholder for bining in 2D
    #if plotstyle is not None:
    #    if verbose:
    #        print('plotstyle: ', plotstyle)
    #    plt.plot(xdata, ydata, plotstyle,
    #             markeredgecolor=None,
    #             markersize=markersize,
    #             linestyle='None')
    #plotid.plotid()

    if debug:
        print()
        print('point plotting complete')
        print('Elapsed time(secs): ',time.time() - t0, lineno())

    if projection == 'cartesian':
        if rarange is None:
            plt.xlim([np.min(xdata), np.max(xdata)])
        if rarange is not None:
            plt.xlim(rarange)

        if decrange is None:
            plt.ylim([np.min(ydata), np.max(ydata)])
        if decrange is not None:
            plt.ylim(decrange)

    plt.xlabel('RA')
    if xlabel != None:
        plt.xlabel(xlabel)

    plt.ylabel('Dec')
    if ylabel != None:
        plt.ylabel(ylabel)
    if title != None:
        plt.title(title)
    if suptitle != None:
        plt.suptitle(suptitle)

    plt.grid()
    if legend:
        plt.legend()

    if not noplotid:
        plotid()

    if aspect == 'equal':
        plt.axes().set_aspect('equal')

    if showplot:
        plt.show()

    if plotfile is None and plotfile_prefix is None:
        plotfile_prefix = 'plot'

    plotfile = plotfile_prefix + '_' + projection + '_radec.png'

    if debug:
        print('Next save the plot')
        print('Elapsed time(secs): ',time.time() - t0, lineno())

    if savefig:
        print('Saving: ', plotfile)
        plt.savefig(plotfile)

    print('Close the plot')
    print('Elapsed time(secs): ',time.time() - t0, lineno())
    plt.close()

    if debug:
        print()
        print('plot_radec complete')
        print('Elapsed time(secs): ',time.time() - t0, lineno())
        print()

    return


if __name__ == "__main__":
    """
    Example and tests

    """
    print('Need to add a demo here; see my astropy plot_galactic.py')
