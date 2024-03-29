def xmatch_checkplots0(ra1, dec1,
                       ra2, dec2,
                       width=10.0,
                       binsize=1.0,
                       saveplot=True,
                       markersize=1.0,
                       plotfile='',
                       suptitle='',
                       **kwargs):

    """
    Based on code by Chris Desira
    """

    import time
    import inspect

    import numpy as np

    import matplotlib.pyplot as plt

    from astropy import stats
    from astropy.coordinates import SkyCoord
    from astropy import units as u

    from librgm.plotid import plotid

    now = time.localtime(time.time())
    datestamp = time.strftime("%Y%m%d", now)
    function_name = inspect.stack()[0][3]

    lineno = str(inspect.stack()[0][2])
    print(mk_timestamp(), function_name, lineno + ':')
    print(function_name + '.saveplot:', saveplot)
    print(function_name + '.plotfile:', plotfile)
    print(function_name + '.prefix:  ', plotfile_prefix)
    print(len(ra1), len(ra2))

    rmax = width

    print('RA1 range:', np.min(ra1), np.max(ra1))
    print('Dec1 range:', np.min(dec1), np.max(dec1))
    print('RA2 range:', np.min(ra2), np.max(ra2))
    print('Dec2 range:', np.min(dec2), np.max(dec2))

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

    itest = (np.abs(dra) < rmax) & (np.abs(ddec) < rmax)

    dra = dra[itest]
    ddec = ddec[itest]

    skycoord_object1 = SkyCoord(ra1, dec1, unit=('degree', 'degree'),
        frame='icrs')
    skycoord_object2 = SkyCoord(ra2, dec2, unit=('degree', 'degree'),
        frame='icrs')

    skycoord_object1 = skycoord_object1[itest]
    skycoord_object2 = skycoord_object2[itest]

    separations = skycoord_object1.separation(skycoord_object2)

    med = np.median(separations.arcsec)
    ndata = len(separations)
    mad = stats.median_absolute_deviation(separations.arcsec)
    mad_std = stats.mad_std(separations.arcsec)

    fig = plt.figure(1, figsize=(10, 5))

    plt.suptitle(suptitle, size=10)

    ax1=fig.add_subplot(1,2,1)

    xdata = separations.arcsec

    n, b, patches = ax1.hist(xdata, bins=rmax/binsize,
                             range=[0.0, rmax],
                             color='green', alpha=0.5)

    bin_min = np.where(n == n.min())


    ax1.locator_params(axis='x', nbins=4)

    s04 = '# = %i'% ndata
    ax1.annotate(s04,(0.28,0.90) , xycoords = 'axes fraction',size=8)

    s01 = 'Median = %.2f' % med
    ax1.annotate(s01,(0.28,0.85) , xycoords = 'axes fraction',size=8)

    ax1.set_xlabel('Pariwise separation (arcsec)')
    ax1.set_ylabel('Frequency per bin')

    ax2 = fig.add_subplot(1,2,2, aspect='equal')

    alpha = 1.0
    ax2.plot(difference_ra,difference_dec,'oc',
             markersize=markersize,
             markeredgewidth=0.0,
             alpha=alpha) #0.5 smallest size

    ax2.axis([-1.0*rmax, rmax,-1.0*rmax, rmax])
    ax2.locator_params(axis='x',nbins=4)
    ax2.set_xlabel('Delta RA')
    ax2.set_ylabel('Delta Dec')
    s11 = 'Self-xmatch'
    ax2.annotate(s11,(0.45,0.95) , xycoords = 'axes fraction',size=8)
    s1 = '# of Objects = %i' % ndata
    ax2.annotate(s1,(0.45,0.90) , xycoords = 'axes fraction',size=8)
    s7 = 'MAD = %.2f' % mad
    ax2.annotate(s7,(0.45,0.85) , xycoords = 'axes fraction',size=8)
    s3 = 'sigma_MAD = %.2f' % mad_std
    ax2.annotate(s3,(0.45,0.80) , xycoords = 'axes fraction',size=8)

    fig.tight_layout()
    ax2.grid()

    fig.subplots_adjust(top=0.88)

    # make room for the plotid on right edge
    fig.subplots_adjust(right=0.95)
    plotid()

    if plotfile != None:
        print('Saving plotfile:', plotfile)
        plt.savefig(plotfile)

    if ('save' in kwargs):
        path_to_save = str(kwargs['save'])
        plt.savefig(path_to_save, dpi=150)
    else:
        plt.show()
