from __future__ import (division, print_function)
#  Forked from Sophie Reed's version on 20160319
import time

import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.stats import mad_std

#sys.path.append("/home/rgm/soft/python/lib/")
from librgm.plotid import plotid
from librgm.mk_timestamp import mk_timestamp
#from librgm.plot_radec import plot_radec
#from librgm.xmatch_checkplot import xmatch_checkplot
#from librgm import stats


def xmatch_checkplot(ra1, dec1, ra2, dec2,
                     figsize = (7.0, 7.0),
                     width=10.0,
                     gtype="all",
                     add_plotid=True,
                     prefix=None,
                     saveplot=True,
                     plotfile=None,
                     plotfile_prefix=None,
                     title=None,
                     suptitle=None):
    """ Makes checkplot for catalogue xmatch results

    Forked from Sophie Reed's version on 20160319

    uses hist2d; a point based option would be useful

    Plot can either be square, the square inscribes the circle.
    Or all which has all the points in the matching circle.
    Square make the histograms more comparable.

    Compares RA_main and DEC_main columns with RA and Dec columns in the
    format output by the matching codes. Eg. RA_ + survey.

    Width needs to be in arcsecs
    """
    import math
    import time
    import inspect

    import numpy as np

    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.colors import LogNorm

    # import stats
    # import plotid

    now = time.localtime(time.time())
    datestamp = time.strftime("%Y%m%d", now)
    function_name = inspect.stack()[0][3]

    lineno = str(inspect.stack()[0][2])
    print(mk_timestamp(), function_name, lineno + ':')
    print(function_name + '.saveplot:', saveplot)
    print(function_name + '.plotfile:', plotfile)
    print(function_name + '.prefix:  ', plotfile_prefix)
    print(len(ra1), len(ra2))

    ndata = len(ra1)
    rmax = width

    # compute Delta RA and Delta Dec in arcsecs
    # ra, dec assumed in have astropy units of degrees
    skycoord1 = SkyCoord(ra1, dec1)
    skycoord2 = SkyCoord(ra2, dec2)
    print(skycoord1[0])
    print(skycoord2[0])
    dra, ddec = skycoord1.spherical_offsets_to(skycoord2)
    dr = skycoord1.separation(skycoord2)
    print(len(dra))
    print(dra[0])
    print(ddec[0])

    dra = dra.arcsecond
    ddec = ddec.arcsecond
    dr = dr.arcsecond

    itest = np.where(dr < rmax)
    print('Number within match radius:', len(itest), len(dr[itest]), rmax)
    ndata_halfrmax = len(dr[np.where(dr < (rmax*0.5))])
    ndata_rmax = len(dr[np.where(dr < rmax)])
    ndata_2rmax = len(dr[np.where(dr < (2*rmax))])
    ndata_4rmax = len(dr[np.where(dr < (4*rmax))])

    print('Number of match with r < 0.5*rmax:', ndata_halfrmax)
    print('Number of match with r < rmax:', ndata_rmax,
          ndata_rmax - ndata_halfrmax)
    print('Number of match with r < 2.0*rmax:', ndata_2rmax,
                    ndata_2rmax - ndata_rmax)
    print('Number of match with r < 4.0*rmax:', ndata_4rmax,
          ndata_4rmax - ndata_2rmax)

    ndata_dradec_max = len(dr[np.where(
        (np.abs(dra) < rmax) & (np.abs(ddec) < rmax))])
    print('Number of match with radec < abs(rmax):', ndata_dradec_max)

    dra = dra[itest]
    ddec = ddec[itest]
    dr = dr[itest]

    RA_med = np.median(dra)
    DEC_med = np.median(ddec)
    RA_mad_std = mad_std(dra)
    DEC_mad_std = mad_std(ddec)

    print("Number of matchs", len(dra))
    print("RA median offset", RA_med)
    print("Dec median offset", DEC_mad_std)
    print("RA Sigma(MAD)", RA_mad_std)
    print("Dec Sigma(MAD)", DEC_mad_std)

    print("RA median error", RA_mad_std / math.sqrt(len(dr)),
          "Dec median error", DEC_mad_std / math.sqrt(len(dr)))

    print("dRA range:", np.min(dra), np.max(dra))
    print("dDec range:", np.min(ddec), np.max(ddec))

    xlimits = np.asarray([-1.0*width, width])
    ylimits = np.asarray([-1.0*width, width])
    limits = np.asarray([xlimits, ylimits])
    print(xlimits[0], xlimits[1])
    print(dra.dtype)
    print(dra.shape)
    print(xlimits.dtype)
    print(xlimits.shape)
    # itest = (xs > xlimits[0] & xs < xlimits[1])
    # xs = xs[itest]
    # itest = (ys > ylimits[0] & ys < ylimits[1])
    # ys = ys[itest]

    print('limits:', limits)
    print('width:', width)

    # GridSpec(nrows, ncols, figure=None,
    #          left=None, bottom=None, right=None, top=None,
    #          wspace=None, hspace=None,
    #          width_ratios=None,height_ratios=None)
    gs = gridspec.GridSpec(2, 2,
                           hspace=0.05, wspace=0.05,
                           width_ratios=[2, 1], height_ratios=[1, 2])
    fig = plt.figure(figsize=figsize)

    # Delta RA Histogram
    ax1 = plt.subplot(gs[0])
    ax1.hist(dra, bins=100, color="r", range=xlimits)
    plt.axvline(0.0, linestyle='dashed')
    ax1.set_xlim(xlimits)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.set_ylabel("Number")


    # Delta RA versus Delta Dec distribution
    ax2 = plt.subplot(gs[2])
    # ax2.plot(xs, ys, "k+")
    if len(dra) > 100:
        plt.hist2d(dra, ddec, bins=100,
                   cmap="binary",
                   norm=LogNorm(),
                   range=limits)
        plt.grid('true')
    else:
        plt.plot(dra, ddec, "k.", ms=2)


    plt.axvline(0.0, linestyle='dashed')
    plt.axhline(0.0, linestyle='dashed')
    ax2.set_ylim(-1*width, width)
    ax2.set_xlim(-1*width, width)
    ax2.set_xlabel('Delta RA /"')
    ax2.set_ylabel('Delta Dec /"')


    #labels1 = ax2.get_xticks()
    #ax2.set_xticklabels(labels1, rotation=270)

    # Delta Dec
    if suptitle is None:
        fig.suptitle("Errors in matching: " +
                     suptitle + ': ' + str(ndata), fontsize='small')

    if suptitle is not None:
        fig.suptitle(suptitle + ': ' + str(ndata), fontsize='small')

    ax3 = plt.subplot(gs[3])
    print('limits:', limits)
    ax3.hist(ddec, bins=100, orientation="horizontal", color="r",
        range=ylimits)

    ax3.set_ylim(ylimits)
    # ax3.set_xlabel("Number")
    plt.axhline(0.0, linestyle='dashed')
    ax3.axes.get_yaxis().set_visible(False)
    labels2 = ax3.get_xticks()
    ax3.set_xticklabels(labels2, rotation=270)


    ax4 = plt.subplot(gs[1])
    x0 = 0.0
    fontsize = 'small'
    fontsize = 'medium'
    ax4.annotate("Number of matchs: " +
                 str(len(dra)), xy=(x0, 0.1), size=fontsize)
    ax4.annotate("Median RA offset: {0:.4f}".format(RA_med) +
                 '"', xy=(x0, 0.90), size=fontsize)
    ax4.annotate("Median DEC offset: {0:.4f}".format(DEC_med) +
                 '"', xy=(x0, 0.8), size=fontsize)
    ax4.annotate("RA sigma MAD: {0:.4f}".format(RA_mad_std) +
                 '"', xy=(x0, 0.7), size=fontsize)
    ax4.annotate("DEC sigma MAD: {0:.4f}".format(DEC_mad_std) +
                 '"', xy=(x0, 0.6), size=fontsize)
    ax4.annotate("RA median error: {0:.4f}".
                 format(RA_mad_std / math.sqrt(len(dr))) + '"',
                 xy=(x0, 0.5), size=fontsize)
    ax4.annotate("DEC median error: {0:.4f}".
                 format(DEC_mad_std / math.sqrt(len(dr))) + '"',
                 xy=(x0, 0.4), size=fontsize)

    ax4.axes.get_xaxis().set_visible(False)
    ax4.axes.get_yaxis().set_visible(False)
    ax4.axis('off')
    ax4.set_axis_off()

    if saveplot:
        lineno = str(inspect.stack()[0][2])
        print(mk_timestamp(), function_name, lineno)
        print('plotfile:', plotfile)
        print('plotfile_prefix:', plotfile_prefix)
        if add_plotid:
            # make room for the plotid on right edge
            fig.subplots_adjust(right=0.95)
            # plotid()

        if plotfile is None:
            plotfile = 'match'
        if plotfile_prefix is not None and plotfile is None:
            plotfile = plotfile_prefix + '_match_' + datestamp + '.png'
        if plotfile_prefix is None and plotfile is None:
            plotfile = 'match_' + datestamp + '.png'

        print('Saving: ', plotfile)
        plt.savefig(plotfile)

    plt.show()

    return RA_med, DEC_med
