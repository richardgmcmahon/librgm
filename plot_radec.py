import time

import numpy as np
from matplotlib import pyplot as plt

# from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import astropy.units as units

from librgm.plotid import plotid

def plot_radec(ra=None, dec=None,
               table=None,
               xcolname='ra', ycolname='dec',
               rarange=None,
               decrange=None,
               system='equatorial',
               frame='equatorial',
               projection='cartesian',
               aspect=None,
               figsize=(8.0, 8.0),
               title=None,
               suptitle=None,
               xlabel=None,
               ylabel=None,
               plotlabel='',
               plotstyle=None,
               linestyle=None,
               markersize=None,
               marker='+',
               color='b',
               showplots=False,
               plotfile=None,
               plotfile_prefix=None,
               plotfile_suffix=None,
               noplotid=False,
               legend=True,
               plotdir='./',
               savefig=True,
               overplot=False,
               verbose=False,
               debug=False):


    """

    assumes units are degree

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
    #plt.setp(lines, edgecolors='None')

    plt.figure(num=None, figsize=figsize)
    if not overplot:
        plt.figure(num=None, figsize=figsize)

        if projection == "aitoff":
            plt.subplot(111, projection="aitoff")


    if table is not None:
       ra = table[xcolname]
       dec = table[ycolname]

    if frame == 'equatorial' or system == 'equatorial':
        if projection == 'cartesian':
            xdata = ra
            ydata = dec

        if projection != 'cartesian':
            skycoords = SkyCoord(ra=ra, dec=dec, unit='deg')
            xdata = skycoords.ra.wrap_at(180 * units.deg).radian
            ydata = skycoords.dec.radian

    if str.lower(system) != 'equatorial':
        skycoords = SkyCoord(ra=ra, dec=dec, unit='deg')

        # convert ra, dec to galactic
        if str.lower(system) == 'galactic':
           galactic = skycoords.galactic
           xdata = galactic.l.degree
           ydata = galactic.b.degree

        # convert ra, dec to ecliptic
        if str.lower(system) == 'ecliptic':
           pass


    if verbose or debug:
        print('RA range: ', np.min(xdata), np.max(xdata))
        print('Dec range: ', np.min(ydata), np.max(ydata))
        print('units: ', units)

    if projection == 'equatorial':

        if rarange is None:
            plt.xlim([np.min(xdata), np.max(xdata)])
        if rarange is not None:
            plt.xlim(rarange)

        if decrange is None:
            plt.ylim([np.min(ydata), np.max(ydata)])
        if decrange is not None:
            plt.ylim(decrange)

    if markersize is None:
        markersize=1.0

    ndata=len(xdata)
    print('Number of points:', ndata)
    if plotstyle is None:
        plt.plot(xdata, ydata,
                 marker='o', c=color,
                 linestyle='None',
                 markeredgecolor=color,
                 markersize=markersize,
                 label=plotlabel + str(ndata))

    if plotstyle is not None:
      if verbose: print('plotstyle: ', plotstyle)
      plt.plot(xdata, ydata, plotstyle,
               markeredgecolor=None,
               markersize=markersize)
    #plotid.plotid()


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

    if legend:
        plt.legend()

    plt.grid()

    if not noplotid:
        plotid(progname=True)

    if aspect == 'equal':
        plt.axes().set_aspect('equal')

    if showplots:
        plt.show()

    if plotfile is None and plotfile_prefix is None:
        plotfile_prefix = 'plot'

    plotfile = plotfile_prefix + '_' + projection + '_radec.png'


    if savefig:
        print('Saving: ', plotfile)
        plt.savefig(plotfile)


if __name__ == "__main__":
    """
    Example and tests

    """
    print('Need to add a demo here; see my astropy plot_galactic.py')
