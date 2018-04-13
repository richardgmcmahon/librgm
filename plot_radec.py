import time

import numpy as np
from matplotlib import pyplot as plt

from astropy.coordinates import Angle
import astropy.units as u

from librgm.plotid import plotid

def plot_radec(ra, dec,
               units=None,
               rarange=None,
               decrange=None,
               system='equatorial',
               project='cartesian',
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
               nolegend=False,
               verbose=False,
               plotdir='./',
               savefig=True,
               overplot=False):
   """



   http://docs.astropy.org/en/stable/coordinates/skycoord.html#example-1-plotting-random-data-in-aitoff-projection

   http://www.astropy.org/astropy-tutorials/plot-catalog.html

   skycoords = SkyCoord(ra = ra*u.degree, dec = dec*u.degree)
   galactic = skycoords.galactic
   plot(galactic.l.wrap_at(180*u.deg), galactic.b.wrap_at(180*u.deg))

   """

    #plt.setp(lines, edgecolors='None')

    if plotfile == None: plotfile='radec.png'

    if not overplot:
        plt.figure(num=None, figsize=figsize)

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


    if str.lower(system) != 'equatorial':
        skycoords = SkyCoord(ra = ra*u.degree, dec = dec*u.degree)

    # convert ra, dec to ecliptic
    if str.lower(system) == 'ecliptic':

    # convert ra, dec to galactic
    if str.lower(system) == 'ecliptic':



        skycoords = SkyCoord(ra = ra*u.degree, dec = dec*u.degree)
   galactic = skycoords.galactic
   plot(galactic.l.wrap_at(180*u.deg), galactic.b.wrap_at(180*u.deg))


    xdata=ra
    ydata=dec

    if verbose or debug:
        print('RA range: ', np.min(xdata), np.max(xdata))
        print('Dec range: ', np.min(ydata), np.max(ydata))
        print('units: ', units)

    if rarange is None:
        plt.xlim([min(xdata),max(xdata)])
    if rarange is not None:
        plt.xlim(rarange)

    if decrange is None:
        plt.ylim([min(ydata),max(ydata)])
    if decrange is not None:
        plt.ylim(decrange)

    if markersize is None:
        markersize=1.0

    ndata=len(xdata)

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
       markeredgecolor=None, markersize=markersize)
    #plotid.plotid()


    if verbose:
        print 'Number of data points plotted: ', ndata

    if not nolegend:
        plt.legend()

    plt.grid()

    if not noplotid:
        plotid(progname=True)

    if aspect == 'equal':
        plt.axes().set_aspect('equal')

    if showplots:
        plt.show()

    if savefig:
        print 'Saving: ', plotfile
        plt.savefig(plotfile)
