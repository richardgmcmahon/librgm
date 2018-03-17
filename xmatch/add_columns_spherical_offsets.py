from __future__ import (division, print_function)

import sys

import numpy as np
import scipy.stats as stats

from astropy.table import Table
from astropy.coordinates import (SkyCoord, search_around_sky,
                                 match_coordinates_sky)
from astropy import units as u

import matplotlib.pyplot as plt

import astropy.stats as apstats

sys.path.append('/home/rgm/soft/python/lib/')
from librgm.plotid import plotid


"""


"""
def add_columns_spherical_offsets(table=None,
                                  ra1=None, dec1=None,
                                  ra2=None, dec2=None,
                                  colname_suffix=None,
                                  plot_drarange=None,
                                  plot_ddecrange=None,
                                  plots=False,
                                  colnames=None,
                                  verbose=None,
                                  **kwargs):
    """

    input is ra1, dec1, ra2, ra2 in pairwise match order

    http://docs.astropy.org/en/stable/api/astropy.table.Table.html#astropy.table.Table.add_columns
    http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html
    http://docs.astropy.org/en/stable/coordinates/matchsep.html
    http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord.position_angle

    plots are based on cdesira

    """

    if verbose:
        print('ra1 range:', np.min(ra1), np.max(ra1))
        print('dec1 range:', np.min(dec1), np.max(dec1))

        print('ra2 range:', np.min(ra2), np.max(ra2))
        print('dec2 range:', np.min(dec2), np.max(dec2))

    # convert ra, dec to units of deg
    # technically this is not needed for the astropy matching since
    # astropy supports units
    if ra1.unit != 'deg':
        ra1 = ra1 * u.deg
    if dec1.unit != 'deg':
        dec1 = dec1 * u.deg
    c1 = SkyCoord(ra=ra1, dec=dec1)

    if ra2.unit != 'deg':
        ra2 = ra2 * u.deg
    if dec2.unit != 'deg':
        dec2 = dec2 * u.deg
    c2 = SkyCoord(ra=ra2, dec=dec2)

    if verbose:
        print('ra1 range:', np.min(ra1), np.max(ra1))
        print('dec1 range:', np.min(dec1), np.max(dec1))

        print('ra2 range:', np.min(ra2), np.max(ra2))
        print('dec2 range:', np.min(dec2), np.max(dec2))
        print()

    dra, ddec = c1.spherical_offsets_to(c2)
    sep = c1.separation(c2)
    pa = c1.position_angle(c2)

    # compute the statistics
    print('stats: n, min, max, mean, median, rms, mad_rms')
    sep_mad_std = apstats.mad_std(sep)
    print('sep:', len(sep), np.min(sep.arcsec), np.max(sep.arcsec),
          np.mean(sep.arcsec), np.median(sep.arcsec),
          np.std(sep.arcsec), apstats.mad_std(sep.arcsec))
    print('pa: ', len(pa), np.min(pa.deg), np.max(pa.deg),
          np.mean(pa.deg), np.median(pa.deg),
          np.std(pa.deg), apstats.mad_std(pa.deg))
    print('dra: ', len(dra.arcsec), np.min(dra.arcsec), np.max(dra.arcsec),
          np.mean(dra.arcsec), np.median(dra.arcsec),
          np.std(dra.arcsec), apstats.mad_std(dra.arcsec))
    print('ddec:', len(ddec), np.min(ddec.arcsec), np.max(ddec.arcsec),
          np.mean(ddec.arcsec), np.median(ddec.arcsec),
          np.std(ddec.arcsec), apstats.mad_std(ddec.arcsec))
    print()

    # need to move these outside this function for portability
    if plots:
        # drarange=[-0.5, 0.5]
        # ddecrange=[-0.5, 0.5]
        alpha = 1.0
        markersize = 4.0
        plt.figure(1, figsize=(8.0, 8.0))
        ndata = len(dra)
        plt.plot(dra.arcsec, ddec.arcsec,
                 'oc',
                 markersize=markersize, markeredgewidth=0.0,
                 alpha=alpha, label=str(ndata))
        plt.xlabel('dra (")')
        plt.ylabel('ddec (")')
        if plot_drarange is not None:
            plt.xlim(plot_drarange)
        if plot_ddecrange is not None:
            plt.ylim(plot_ddecrange)
        plt.grid()
        plt.legend()
        plotid()

        dra_mean = np.mean(dra.arcsec)
        dra_median = np.median(dra.arcsec)
        dra_std = np.std(dra.arcsec)
        dra_mad_std = apstats.mad_std(dra.arcsec)

        ddec_mean = np.mean(ddec.arcsec)
        ddec_median = np.median(ddec.arcsec)
        ddec_std = np.std(ddec.arcsec)
        ddec_mad_std = apstats.mad_std(ddec.arcsec)

        s0 = '           dra, ddec'
        plt.annotate(s0,(0.05,0.98) , xycoords = 'axes fraction',size=12)
        s1 = 'mean    = %.3f, %.3f'% (dra_mean, ddec_mean)
        plt.annotate(s1,(0.05,0.94) , xycoords = 'axes fraction',size=12)
        s2 = 'median  = %.3f, %.3f'% (dra_median, ddec_median)
        plt.annotate(s2,(0.05,0.90) , xycoords = 'axes fraction',size=12)
        s3 = 'std     = %.3f, %.3f' % (dra_std, ddec_std)
        plt.annotate(s3,(0.05,0.86) , xycoords = 'axes fraction',size=12)
        s4 = 'mad_std = %.3f, %.3f' % (dra_mad_std, ddec_mad_std)
        plt.annotate(s4,(0.05,0.82) , xycoords = 'axes fraction',size=12)

        if ('plot_title' in kwargs):
            plt.title(str(kwargs['plot_title']), fontsize='medium')
        if ('plot_suptitle' in kwargs):
            plt.suptitle(str(kwargs['plot_suptitle']), fontsize='medium')

        plt.show()

    if colname_suffix is None:
        colname_suffix = ''

    if colname_suffix is not None:
        colname_suffix = '_' + colname_suffix

    # maybe should be in degrees
    table['dRA' + colname_suffix] = dra.arcsec
    table['dDec' + colname_suffix] = ddec.arcsec
    table['dR' + colname_suffix] = sep.arcsec
    table['PA' + colname_suffix] = pa.deg

    return table
