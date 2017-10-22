from __future__ import (division, print_function)

def xmatch_cat(table1=None, table2=None,
               radec1=None, radec2=None,
               nthneighbor=None,
               selfmatch=False,
               colnames_radec1=['ra', 'dec'],
               colnames_radec2=['ra', 'dec'],
               units_radec1=['degree', 'degree'],
               units_radec2=['degree', 'degree'],
               stats=True,
               debug=False,
               verbose=False):
    """RA, Dec nearest xmatch for two lists; returns pointers

    nearest match


    Self match notes:


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

    if selfmatch:
        table2 = table1
        colnames_radec2 = colnames_radec1
        if nthneighbor is None:
            nthneighbor = 2

    if nthneighbor is None:
        nthneighbor = 1

    ra1 = table1[colnames_radec1[0]]
    dec1 = table1[colnames_radec1[1]]
    print('table1: ', colnames_radec1[0], table1[colnames_radec1[0]].unit)
    print('table1: ', colnames_radec1[1], table1[colnames_radec1[1]].unit)

    ra2 = table2[colnames_radec2[0]]
    dec2 = table2[colnames_radec2[1]]
    print('table2: ', colnames_radec2[0], table2[colnames_radec2[0]].unit)
    print('table2: ', colnames_radec2[1], table2[colnames_radec2[1]].unit)


    if stats or verbose or debug:
        print('RA1 range:', np.min(ra1), np.max(ra1))
        print('Dec1 range:', np.min(dec1), np.max(dec1))

        print('RA1 range:', np.min(ra2), np.max(ra2))
        print('Dec1 range:', np.min(dec2), np.max(dec2))


    skycoord1 = SkyCoord(ra1, dec1, unit=units_radec1, frame='icrs')
    skycoord2 = SkyCoord(ra2, dec2, unit=units_radec2, frame='icrs')

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
        print('len(table1):', len(table1))
        print('len(table2):', len(table2))
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

    separation = separation.arcsec

    dr = d2d.arcsec

    print(len(idxmatch), len(dr))

    return idxmatch, dr
