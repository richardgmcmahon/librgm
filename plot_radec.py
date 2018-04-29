from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.coordinates import BarycentricTrueEcliptic
from astropy import units as units

# import private functions
# sys.path.append("/home/rgm/soft/python/lib/")
from librgm.plotid import plotid

def plot_radec(table=None,
               colnames_radec=(None, None),
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
               savefig=True,
               plotfile=None,
               plotfile_prefix=None,
               outpath=None,
               showplot=False,
               verbose=False,
               debug=False):
    """

    assumes units are degree

    subplot projections need angles to be in radians so conversion from
    degrees to radians is needed

    ra, dec can be as lists or table columns

    """
    import time

    t0 = time.time()
    print(frame, projection)
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

    if frame != 'equatorial':
        skycoords = SkyCoord(ra=ra, dec=dec, unit='deg')

    if frame == 'galactic':
        # convert ra, dec to galactic
        galactic = skycoords.galactic
        if projection == 'cartesian':
            xdata = galactic.l.degree
            ydata = galactic.b.degree

        if projection != 'cartesian':
            xdata = galactic.l.wrap_at(180 * units.deg).radian
            ydata = galactic.b.radian

    if frame == 'ecliptic':
        skycoords_ecliptic = skycoords.transform_to(BarycentricTrueEcliptic)
        if projection == 'cartesian':
            xdata = skycoords_ecliptic.lon.degree
            ydata = skycoords_ecliptic.lat.degree

        if projection != 'cartesian':
            xdata = skycoords_ecliptic.lon.wrap_at(180 * units.deg).radian
            ydata = skycoords_ecliptic.lat.radian

    ndata = len(xdata)
    xmin = np.min(xdata)
    xmax = np.max(xdata)
    ymin = np.min(ydata)
    ymax = np.max(ydata)

    print('Number of points:', ndata, type(xdata), type(ydata))
    print(marker, markersize, alpha, color, markeredgecolor)
    plt.plot(xdata, ydata,
             marker=marker, color=color,
             markersize=markersize,
             alpha=alpha,
             markeredgecolor=markeredgecolor,
             linestyle='None',
             label=str(ndata))

    if projection == 'cartesian':
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)

    plt.grid()
    plt.legend(loc='upper right')


    if title is not None:
         plt.title(title)
    if suptitle is not None:
        plt.suptitle(suptitle, fontsize='medium')

    if frame == 'equatorial':
        plt.xlabel('Right Ascension: [degree] ' + xcolname)
        plt.ylabel('Declination: [degree] ' + ycolname)

    if frame == 'galactic':
        plt.xlabel('Galactic Longitude (l) [degree]')
        plt.ylabel('Galactic Latitute (b) [degree]')

    if frame == 'ecliptic':
        plt.xlabel('Ecliptic Longitude [degree]')
        plt.ylabel('Ecliptic Latitute [degree]')

    plotid()

    if plotfile is None and plotfile_prefix is None:
        plotfile_prefix = 'plot'

    plotfile = plotfile_prefix + '_' + projection + '_radec.png'
    if outpath is not None:
        plotfile = outpath + plotfile
    print('Saving:', plotfile)
    plt.savefig(plotfile)

    if showplot:
        plt.show()

    plt.close()

    return
