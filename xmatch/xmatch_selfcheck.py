from __future__ import (division, print_function)

def xmatch_selfcheck(data=None,
                     colnames_radec=['ra', 'dec'],
                     units_radec=['degree', 'degree'],
                     rmax=10.0,
                     binsize=None,
                     plotfile=None,
                     saveplot=True,
                     showplot=False,
                     markersize=2.0,
                     nthneighbor=2,
                     suptitle="",
                     **keyword_parameter):
    """
    Based on check_matching.py by Chris Desira (Summer 2016)

    See also /home/rgm/soft/gaia/check_matching.py

    """

    import time
    import numpy as np

    import matplotlib.pyplot as plt

    from astropy.coordinates import (search_around_sky, SkyCoord,
                                 match_coordinates_sky)

    from astropy.stats import mad_std, median_absolute_deviation

    from librgm.plotid import plotid

    print('__file__', __file__)
    print('__name__', __name__)

    print('colnames_radec:', colnames_radec)
    print('markersize:', markersize)

    t0 = time.time()

    ra = data[colnames_radec[0]]
    dec = data[colnames_radec[1]]
    print('RA range:', np.min(ra), np.max(ra))
    print('Dec range:', np.min(dec), np.max(dec))

    skycoord_objects = SkyCoord(ra, dec, unit=units_radec, frame='icrs')

    # nearest neighbor matches to itself
    # idx is an integer array into the first cordinate array to get the
    # matched points for the second coorindate array.
    # Shape of idx matches the first coordinate array
    print('Elapsed time(secs):', time.time() - t0)
    print('Self xmatch starting:', len(skycoord_objects))
    idx, d2d, d3d = match_coordinates_sky(skycoord_objects,
                                          skycoord_objects,
                                          nthneighbor=nthneighbor)
    print('Self xmatch completed:', len(idx))
    print('Elapsed time(secs):', time.time() - t0)

    #set limits

    separations = np.asarray(d2d.arcsec)
    print('Separation range:', np.min(separations), np.max(separations))
    print('Separation median:', np.median(separations))
    upperlimit = rmax
    upperlimit2 = rmax
    separations_reduced = separations[(separations<=upperlimit)]
    separations_orig = separations[(separations<=upperlimit2)]
    # psfmag_reduced=np.asarray(psfmag)[(separations<=upperlimit)]

    # separations_reduced = separations[(np.asarray(psfmag)<18.0)*(separations<=upperlimit2)]
    # separations_orig = separations[(separations<=upperlimit2)]
    # psfmag_reduced=np.asarray(psfmag)[(np.asarray(psfmag)<18.0)]

    masked_list_ra = np.asarray(skycoord_objects.ra)[(idx)]
    masked_list_dec = np.asarray(skycoord_objects.dec)[(idx)]
    masked_list_ra_cat = np.asarray(skycoord_objects.ra)
    masked_list_dec_cat = np.asarray(skycoord_objects.dec)
    # masked = skycoord_object[idx]
    # dra, ddec = skycoord_object.spherical_offsets_to(masked)
    # sky = SkyCoord(masked_list_ra*u.degree, masked_list_dec*u.degree, frame='icrs')
    # dra, ddec = skycoord_object.spherical_offsets_to(sky)
    # dra=float(dra.to(u.arcsec))
    # ddec=float(dra.to(u.arcsec))

    difference_ra = ((((masked_list_ra_cat-masked_list_ra)*np.cos(np.radians(masked_list_dec_cat))))*3600.0)
    difference_dec = (((masked_list_dec_cat-masked_list_dec))*3600.0)

    median_and_mean = [list(difference_ra), list(difference_dec)]
    median_and_mean = np.asarray(median_and_mean)
    mad_standard = mad_std(median_and_mean)
    mad_median = median_absolute_deviation(median_and_mean)
    length = len(masked_list_ra)
    med = np.median(separations)

    #pylab.title("file: %s"%files,size=14, fontsize='medium')

    fig = plt.figure(1, figsize=(10, 5))

    plt.suptitle(suptitle + 'nthN:' + str(nthneighbor), size=10)

    ax1 = fig.add_subplot(1,2,1)

    if binsize is None:
        bins = int(upperlimit2/0.5)
    if binsize is not None:
        bins = int(rmax/binsize) + 1
    print('bins:', bins)
    hist_range = [0.0, upperlimit2]
    print('hist_range:', hist_range)
    itest = (separations_orig < rmax)
    ndata = len(separations_orig[itest])
    n, b, patches = ax1.hist(separations_orig[itest],
                             bins=bins,
                             label=str(ndata),
                             range=hist_range,
                             color='green', alpha=0.5)
    bin_min = np.where(n == n.min())

    ax1.locator_params(axis='x',nbins=4)
    s0 = 'Matched to self'
    ax1.annotate(s0,(0.28,0.95), xycoords='axes fraction', size=8)

    s04 = '# = %i'%length
    ax1.annotate(s04,(0.28,0.90), xycoords='axes fraction', size=8)

    s01 = 'Median = %.2f' % med
    ax1.annotate(s01,(0.28,0.85), xycoords='axes fraction', size=8)

    ax1.set_xlabel('Pairwise separation (arcseconds)')
    ax1.set_ylabel('Frequency per bin')
    ax1.legend(loc='lower right')

    ax2 = fig.add_subplot(1,2,2, aspect='equal')

    alpha = 1.0
    itest = (np.abs(difference_ra) < rmax) & \
            (np.abs(difference_dec) < rmax)
    ndata = len(difference_ra[itest])
    ax2.plot(difference_ra[itest], difference_dec[itest],
             'oc', label = str(ndata),
             markersize=markersize,
             markeredgewidth=0.0,
             alpha=alpha) #0.5 smallest size

    ax2.axis([-1.0*rmax, rmax,-1.0*rmax, rmax])
    ax2.locator_params(axis='x',nbins=4)
    ax2.set_xlabel('Delta RA')
    ax2.set_ylabel('Delta Dec')
    s11 = 'Self-xmatch'
    ax2.annotate(s11,(0.45,0.95) , xycoords = 'axes fraction',size=8)
    s1 = '# of Objects = %i' % length
    ax2.annotate(s1,(0.45,0.90) , xycoords = 'axes fraction',size=8)
    s7 = 'MAD = %.2f' % mad_median
    ax2.annotate(s7,(0.45,0.85) , xycoords = 'axes fraction',size=8)
    s3 = 'sigma_MAD = %.2f' % mad_standard
    ax2.annotate(s3,(0.45,0.80) , xycoords = 'axes fraction',size=8)


    fig.tight_layout()
    ax2.grid()
    ax2.legend(loc='lower right')

    fig.subplots_adjust(top=0.88)

    # make room for the plotid on right edge
    fig.subplots_adjust(right=0.95)
    plotid()

    if plotfile is None:
        plotfile = 'xmatch_selfcheck.png'

    if plotfile != None and saveplot:
        print('Saving plotfile:', plotfile)
        plt.savefig(plotfile)

    if showplot:
        plt.show()

    plt.close()

    return idx
