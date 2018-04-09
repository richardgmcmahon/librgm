from __future__ import (division, print_function)
#  Forked from Sophie Reed's version on 20160319
import time

from astropy.stats import mad_std

#sys.path.append("/home/rgm/soft/python/lib/")
from librgm.plotid import plotid
from librgm.mk_timestamp import mk_timestamp
#from librgm.plot_radec import plot_radec
#from librgm.xmatch_checkplot import xmatch_checkplot
#from librgm import stats


def xmatch_checkplot(ra1, dec1, ra2, dec2,
                     figsize = (6.0, 6.0),
                     width=10.0,
                     gtype="all", add_plotid=True, prefix=None,
                     saveplot=True,
                     plotfile="", plotfile_prefix=None,
                     title="",
                     suptitle=""):
    """ Makes checkplot for catalogue xmatch results

    Forked from Sophie Reed's version on 20160319

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

    ndata = len(ra1)

    n = 0
    xs = []
    ys = []
    while n < len(ra1):
        x = (ra1[n] - ra2[n]) * \
             math.cos((ra1[n] + ra2[n]) * math.pi / 360.0) * 3600.0
        y = (dec1[n] - dec2[n]) * 3600.0

        if not np.isnan(x) and not np.isnan(y):
            xs.append(x)
            ys.append(y)
        n += 1

    n = 0
    xs_s = []
    ys_s = []

    if gtype == "square":
        w = width / math.sqrt(2.0)
        while n < len(xs):
            x = xs[n]
            y = ys[n]
            if x <= w and x >= -w and y <= w and y >= -w:
                xs_s.append(xs[n])
                ys_s.append(ys[n])
            n += 1

        xs = xs_s
        ys = ys_s

    xs1 = list(xs) + []
    ys1 = list(ys) + []

    RA_med = np.median(xs1)
    DEC_med = np.median(ys1)
    RA_mad_std = mad_std(xs1)
    DEC_mad_std = mad_std(ys1)

    print("Number of points", len(xs))
    print("RA median offset", RA_med, "Dec median offset", DEC_mad_std)
    print("RA Sigma(MAD)", RA_mad_std, "Dec Sigma(MAD)", DEC_mad_std)
    print("RA median error", RA_mad_std / math.sqrt(len(xs)),
          "Dec median error", DEC_mad_std / math.sqrt(len(ys)))
    print("dRA range:", np.min(xs1), np.max(xs1))
    print("dDec range:", np.min(ys1), np.max(ys1))
    print()
    if len(xs) == 0:
        print("No matches")
        return RA_med, DEC_med

    xs = np.asarray(xs)
    ys = np.asarray(ys)
    xlimits = np.asarray([-1.0*width, width])
    ylimits = np.asarray([-1.0*width, width])
    limits = np.asarray([xlimits, ylimits])
    print(xlimits[0], xlimits[1])
    print(xs.dtype)
    print(xs.shape)
    print(xlimits.dtype)
    print(xlimits.shape)
    # itest = (xs > xlimits[0] & xs < xlimits[1])
    # xs = xs[itest]
    # itest = (ys > ylimits[0] & ys < ylimits[1])
    # ys = ys[itest]

    print('limits:', limits)
    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 2])
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(gs[0])
    ax1.hist(xs, bins=100, color="r", range=xlimits)
    ax1.set_xlim(xlimits)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.set_ylabel("Number")

    ax2 = plt.subplot(gs[2])
    # ax2.plot(xs, ys, "k+")
    if len(xs) > 100:
        plt.hist2d(xs, ys, bins=100, cmap="binary", norm=LogNorm(),
            range=limits)
    else:
        plt.plot(xs, ys, "k.", ms=2)
    ax2.set_ylim(-1*width, width)
    ax2.set_xlim(-1*width, width)
    ax2.set_xlabel('Delta RA /"')
    ax2.set_ylabel('Delta Dec /"')
    labels1 = ax2.get_xticks()
    ax2.set_xticklabels(labels1, rotation=270)

    if suptitle is None:
        fig.suptitle("Errors in matching: " +
                     suptitle + ': ' + str(ndata), fontsize='small')

    if suptitle is not None:
        fig.suptitle(suptitle + ': ' + str(ndata), fontsize='small')

    ax3 = plt.subplot(gs[3])
    print('limits:', limits)
    ax3.hist(ys, bins=100, orientation="horizontal", color="r",
        range=ylimits)

    ax3.set_ylim(ylimits)
    ax3.set_xlabel("Number")
    ax3.axes.get_yaxis().set_visible(False)
    labels2 = ax3.get_xticks()
    ax3.set_xticklabels(labels2, rotation=270)

    ax4 = plt.subplot(gs[1])
    ax4.annotate("Number of points: " +
                 str(len(xs)), xy=(0.01, 0.1), size="small")
    ax4.annotate("RA offset: {0:.4f}".format(RA_med) +
                 '"', xy=(0.01, 0.90), size="small")
    ax4.annotate("DEC offset: {0:.4f}".format(DEC_med) +
                 '"', xy=(0.01, 0.8), size="small")
    ax4.annotate("RA sigma MAD: {0:.4f}".format(RA_mad_std) +
                 '"', xy=(0.01, 0.7), size="small")
    ax4.annotate("DEC sigma MAD: {0:.4f}".format(DEC_mad_std) +
                 '"', xy=(0.01, 0.6), size="small")
    ax4.annotate("RA median error: {0:.4f}".
                 format(RA_mad_std / math.sqrt(len(xs))) + '"',
                 xy=(0.01, 0.5), size="small")
    ax4.annotate("DEC median error: {0:.4f}".
                 format(DEC_mad_std / math.sqrt(len(ys))) + '"',
                 xy=(0.01, 0.4), size="small")
    ax4.annotate("RA sigma MAD: {0:.4f}".format(RA_mad_std) +
                 '"', xy=(0.01, 0.3), size="small")
    ax4.annotate("DEC sigma MAD: {0:.4f}".format(DEC_mad_std) +
                 '"', xy=(0.01, 0.2), size="small")

    ax4.axes.get_xaxis().set_visible(False)
    ax4.axes.get_yaxis().set_visible(False)

    if saveplot:
        lineno = str(inspect.stack()[0][2])
        print(mk_timestamp(), function_name, lineno)
        print('plotfile:', plotfile)
        print('plotfile_prefix:', plotfile_prefix)
        if add_plotid:
            # make room for the plotid on right edge
            fig.subplots_adjust(right=0.95)
            plotid()

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
