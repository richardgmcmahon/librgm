from __future__ import (division, print_function)

def xmatch_groups(table1=None, table2=None,
                  colnames_radec1=['ra', 'dec'],
                  colnames_radec2=['ra', 'dec'],
                  units_radec1=['degree', 'degree'],
                  units_radec2=['degree', 'degree'],
                  selfmatch=False,
                  rmax=10.0,
                  stats=True,
                  debug=False,
                  verbose=False,
                  checkplot=True,
                  join=False,
                  plotfile_label=''):
    """Group RA, Dec xmatch for two lists; returns pointers

    Topcat

    http://www.star.bris.ac.uk/~mbt/topcat/sun253/sun253.html#matchAlgorithm

    http://www.star.bris.ac.uk/~mbt/topcat/sun253/sun253.html#matchCriteria


    all matchs within a radius

    https://www.sites.google.com/site/mrpaulhancock/blog/theage-oldproblemofcross-matchingastronomicalsources

    http://www.astropy.org/astropy-tutorials/Coordinates.html

    see:
    http://docs.astropy.org/en/stable/_modules/astropy/table/groups.html


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
    print('plotfile_label:', plotfile_label)

    import xmatch_checkplot
    import xmatch_checkplot0

    if selfmatch:
        table2 = table1
        colnames_radec2 = colnames_radec1

    ra1 = table1[colnames_radec1[0]]
    dec1 = table1[colnames_radec1[1]]

    ra2 = table2[colnames_radec2[0]]
    dec2 = table2[colnames_radec2[1]]

    if stats or verbose or debug:
        print('RA1 range:', np.min(ra1), np.max(ra1))
        print('Dec1 range:', np.min(dec1), np.max(dec1))

        print('RA1 range:', np.min(ra2), np.max(ra2))
        print('Dec1 range:', np.min(dec2), np.max(dec2))

    skycoord1 = SkyCoord(ra1, dec1, unit=units_radec1, frame='icrs')
    skycoord2 = SkyCoord(ra2, dec2, unit=units_radec1, frame='icrs')

    """
    idx is an integer array into the first cordinate array to get the
    matched points for the second coorindate array.
    Shape of idx matches the first coordinate array

    http://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html
    astropy.coordinates.search_around_sky(
        coords1, coords2, seplimit, storekdtree='kdtree_sky'

    Returns:

    idx1 : integer array
           Indices into coords1 that matches to the corresponding element of
           idx2. Shape matches idx2.

    idx2 : integer array
           Indices into coords2 that matches to the corresponding element of
           idx1. Shape matches idx1.
    sep2d : Angle

    The on-sky separation between the coordinates. Shape matches idx1 and idx2.

    """

    idxmatch1, idxmatch2, d2d, d3d = \
        skycoord1.search_around_sky(skycoord2,
                                    rmax * u.arcsec)

    separation = skycoord1[idxmatch1].separation(skycoord2[idxmatch2])

    dra, ddec = \
        skycoord1[idxmatch2].spherical_offsets_to(skycoord2[idxmatch2])

    if stats or verbose or debug:
        print('len(table1):', len(table1))
        print('len(table2):', len(table2))
        print()
        print('len(idxmatch1):', len(idxmatch1))
        print('idxmatch1 range:', np.min(idxmatch1), np.max(idxmatch1))
        print()
        print('len(idxmatch2):', len(idxmatch2))
        print('idxmatch1 range:', np.min(idxmatch2), np.max(idxmatch2))
        print()
        print('d2d range (arcsec):', np.min(d2d).arcsec, np.max(d2d).arcsec)
        print('d2d median (arcsec):', np.median(d2d).arcsec)

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
        suptitle = plotfile_label + 'nthN:' + str(nthneighbor)
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

    print(len(idxmatch1), len(idxmatch2), len(dr))

    return idxmatch1, idxmatch2, d2d.arcsec
