from __future__ import (division, print_function)

def xmatch_cat(data1=None, data2=None,
               nthneighbor=1,
               selfmatch=False,
               colnames_radec1=['ra', 'dec'],
               colnames_radec2=['ra', 'dec'],
               units_radec1=['degree', 'degree'],
               units_radec2=['degree', 'degree'],
               rmax=10.0,
               rmax2=None,
               stats=True,
               debug=False,
               verbose=False,
               checkplot=True,
               join=False,
               plotfile_label=''):
    """RA, Dec xmatch for two lists; returns pointers

    nearest match

    """

    import numpy as np
    import matplotlib.pyplot as plt

    from astropy.table import Table, hstack
    from astropy.coordinates import SkyCoord
    from astropy.coordinates import search_around_sky, match_coordinates_sky
    from astropy import units as u
    from astropy.stats import mad_std, median_absolute_deviation

    print('__file__:', __file__)
    print('__name__:', __name__)
    print('colnames_radec1:', colnames_radec1)
    print('colnames_radec2:', colnames_radec2)
    print('plotfile_label:', plotfile_label)

    import xmatch_checkplot
    import xmatch_checkplot0

    if selfmatch:
        data2 = data1
        colnames_radec2 = colname_radec1
        nthneighbor=2

    # print(data1[0])
    # print(data2[0])

    ra1 = data1[colnames_radec1[0]]
    dec1 = data1[colnames_radec1[1]]

    ra2 = data2[colnames_radec2[0]]
    dec2 = data2[colnames_radec2[1]]

    if stats or verbose or debug:
        print('RA1 range:', np.min(ra1), np.max(ra1))
        print('Dec1 range:', np.min(dec1), np.max(dec1))

        print('RA1 range:', np.min(ra2), np.max(ra2))
        print('Dec1 range:', np.min(dec2), np.max(dec2))


    skycoord1 = SkyCoord(ra1, dec1, unit=units_radec1, frame='icrs')
    skycoord2 = SkyCoord(ra2, dec2, unit=units_radec1, frame='icrs')

    # idx is an integer array into the first cordinate array to get the
    # matched points for the second coorindate array.
    # Shape of idx matches the first coordinate array
    idxmatch, d2d, d3d = match_coordinates_sky(skycoord1,
                                               skycoord2,
                                               nthneighbor=nthneighbor)

    # alternative 'method' form
    # idxmatch, d2d, d3d = skycoord1.match_to_catalog_sky(skycoord2)

    separation = skycoord1.separation(skycoord2[idxmatch])

    dra, ddec = \
        skycoord1.spherical_offsets_to(skycoord2[idxmatch])

    if stats or verbose or debug:
        print('len(data1):', len(data1))
        print('len(data2):', len(data2))
        print('len(idxmatch):', len(idxmatch))
        print('idxmatch range:', np.min(idxmatch), np.max(idxmatch))
        print('d2d range:', np.min(d2d), np.max(d2d))
        print('d2d range:', np.min(d2d).arcsec, np.max(d2d).arcsec)
        print('d2d median:', np.median(d2d).arcsec)

        median_separation = np.median(separation).arcsec
        mad_std_separation = mad_std(separation.arcsec)
        print('dR range (arcsec):',
              np.min(separation.arcsec), np.max(separation.arcsec))
        print('dR mean, std (arcsec):',
              np.mean(separation).arcsec, np.std(separation).arcsec)
        print('dR  median, mad_std (arcsec):',
              median_separation, mad_std_separation)
        print()

        median_dra = np.median(dra).arcsec
        mad_std_dra = mad_std(dra.arcsec)
        print('dRA min, max:',
              np.min(dra).arcsec, np.max(dra).arcsec)
        print('dRA mean, std:',
              np.mean(dra).arcsec, np.std(dra).arcsec)
        print('dRA median, mad_std:',
              median_dra, mad_std_dra)
        print()

        median_ddec = np.median(ddec).arcsec
        mad_std_ddec = mad_std(ddec.arcsec)
        print('dDec min, max:',
              np.min(ddec).arcsec, np.max(ddec).arcsec)
        print('dDec mean, std:',
              np.mean(ddec).arcsec, np.std(ddec).arcsec)
        print('dDec median, mad_std:',
              median_ddec, mad_std_ddec)
        print()


    if checkplot:
        suptitle = plotfile_label
        plotfile = 'xmatch_cat' + plotfile_label + '_a_checkplot.png'

        ra2_xmatch = ra2[idxmatch]
        dec2_xmatch = dec2[idxmatch]

        xmatch_checkplot.xmatch_checkplot(
            ra1, dec1, ra2_xmatch, dec2_xmatch,
            width=rmax,
            gtype='square',
            saveplot=True,
            plotfile=plotfile,
            suptitle=suptitle)
        plt.close()

        plotfile = 'xmatch_cat' + plotfile_label + '_b_checkplot0.png'
        xmatch_checkplot0.xmatch_checkplot0(
                      ra1, dec1, ra2_xmatch, dec2_xmatch,
                      width=10.0,
                      gtype='square',
                      saveplot=True,
                      plotfile=plotfile,
                      suptitle=suptitle)
        plt.close()

    idx1 = idxmatch
    idx2 = []
    separation = separation.arcsec

    dr = d2d.arcsec

    print(len(idxmatch), len(dr))

    return idxmatch, dr
