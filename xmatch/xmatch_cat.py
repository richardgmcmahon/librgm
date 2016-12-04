from __future__ import (division, print_function)

def xmatch_cat(data1=None, data2=None,
               nthneighbor=1,
               colnames_radec1=['ra', 'dec'],
               colnames_radec2=['ra', 'dec'],
               units_radec1=['degree', 'degree'],
               units_radec2=['degree', 'degree'],
               rmax=10.0,
               stats=True,
               debug=False,
               verbose=False,
               checkplot=True,
               plotfile_label="",
               **kwargs):
    """RA, Dec xmatch for two lists; returns pointers

    nearest match

    """

    import numpy as np
    import matplotlib.pyplot as plt

    from astropy.coordinates import SkyCoord
    from astropy.coordinates import search_around_sky, match_coordinates_sky
    from astropy import units as u

    print('__file__:', __file__)
    print('__name__:', __name__)
    print('colnames_radec1:', colnames_radec1)
    print('colnames_radec2:', colnames_radec2)
    print('plotfile_label:', plotfile_label)

    import xmatch_checkplot
    import xmatch_checkplot0


    # print(data1[0])
    # print(data2[0])

    ra1 = data1[colnames_radec1[0]]
    dec1 = data1[colnames_radec1[1]]

    ra2 = data2[colnames_radec2[0]]
    dec2 = data2[colnames_radec2[1]]

    skycoord1 = SkyCoord(ra1, dec1, unit=units_radec1, frame='icrs')
    skycoord2 = SkyCoord(ra2, dec2, unit=units_radec1, frame='icrs')

    # idx is an integer array into the first cordinate array to get the
    # matched points for the second coorindate array.
    # Shape of idx matches the first coordinate array
    idx, d2d, d3d = match_coordinates_sky(skycoord1,
                                          skycoord2,
                                          nthneighbor=nthneighbor)

    separation = skycoord1.separation(skycoord2[idx])

    dra, ddec = \
        skycoord1.spherical_offsets_to(skycoord2[idx])


    # alternative 'method' form
    # idxmatch, d2d, d3d = skycoord1.match_to_catalog_sky(skycoord2)

    if stats or verbose or debug:
        print('Using: match_coordinates_sky')
        print('radec_veron.match_to_catalog_sky(radec_dr7qso)')
        print('len(data1):', len(data1))
        print('len(data2):', len(data2))
        print('len(idx):', len(idx))
        print('idx range:', np.min(idx), np.max(idx))
        print('d2d range:', np.min(d2d), np.max(d2d))
        print('d2d range:', np.min(d2d).arcsec, np.max(d2d).arcsec)
        print('d2d median:', np.median(d2d).arcsec)


        median_separation = np.median(separation).arcsec
        print('Median separation (arc seconds):', median_separation)


        median_dra = np.median(dra).arcsec
        print('Median dRA (arc seconds):', median_dra)

        median_ddec = np.median(ddec).arcsec
        print('Median dDec (arc seconds):', median_ddec)

    suptitle = plotfile_label
    plotfile = 'xmatch_cat' + plotfile_label + '_a_checkplot.png'

    ra2_xmatch = ra2[idx]
    dec2_xmatch = dec2[idx]

    xmatch_checkplot.xmatch_checkplot(ra1, dec1, ra2_xmatch, dec2_xmatch,
                     width=rmax,
                     gtype='square',
                     saveplot=True,
                     plotfile=plotfile,
                     suptitle=suptitle)
    plt.close()

    plotfile = 'xmatch_cat' + plotfile_label + '_b_checkplot0.png'
    xmatch_checkplot0.xmatch_checkplot0(ra1, dec1, ra2_xmatch, dec2_xmatch,
                      width=10.0,
                      gtype='square',
                      saveplot=True,
                      plotfile=plotfile,
                      suptitle=suptitle)
    plt.close()

    idx1 = idx
    idx2 = []
    separation = separation.arcsec
    dr = d2d.arcsec

    print(len(idx), len(dr))

    return idx , dr
