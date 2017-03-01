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

    from astropy.table import Table, Column, hstack
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
    if selfmatch:
        itest = idxmatch1 != idxmatch2
        print('selfmatch: Number of matchs within rmax:',
            len(idxmatch1[itest]), len(table1), rmax)
        idxmatch1 = idxmatch1[itest]
        idxmatch2 = idxmatch2[itest]
        d2d = d2d[itest]
        d3d = d3d[itest]


    isort = np.argsort(idxmatch1)
    idxmatch1 = idxmatch1[isort]
    idxmatch2 = idxmatch2[isort]

    separation = skycoord1[idxmatch1].separation(skycoord2[idxmatch2])
    pa = skycoord1[idxmatch1].position_angle(skycoord2[idxmatch2])
    dra, ddec = \
        skycoord1[idxmatch1].spherical_offsets_to(skycoord2[idxmatch2])

    idxmatch1_unique, index, counts = np.unique(
        idxmatch1, return_index=True, return_counts=True)
    data = counts
    binwidth = 1
    plt.hist(counts, bins=range(min(data), max(data) + binwidth, binwidth))
    plt.show()

    idxmatch2_unique, index, counts = np.unique(
        idxmatch2, return_index=True, return_counts=True)
    data = counts
    binwidth = 1
    plt.hist(counts, bins=range(min(data), max(data) + binwidth, binwidth))
    plt.show()

    print('table1 columns:', len(table1.colnames))
    print('table2 columns:', len(table2.colnames))

    # result = hstack([table1[idxmatch1], table1[idxmatch2]])
    # print('result columns:', len(result.colnames))
    # nrows = len(result)

    xmatch1 = table1[idxmatch1]
    xmatch2 = table2[idxmatch2]

    nrows = len(xmatch1)
    groupid = np.empty(nrows, dtype=int)
    groupsize = np.zeros(nrows, dtype=int)

    for isource, idxsource in enumerate(idxmatch1):
        if isource == 0:
            igroup = 1
            groupid[isource] = igroup
            if groupsize[isource] == 0:
                groupsize[isource] = 2

        if isource != 0:
            if idxmatch1[isource] == idxmatch1[isource - 1]:
                groupsize[isource] = groupsize[isource - 1] + 1
                groupid[isource] = groupid[isource - 1]

            if idxmatch1[isource] != idxmatch1[isource - 1]:
                groupsize[isource] = 2
                igroup = igroup + 1
                groupid[isource] = igroup

    print('Group size range:', np.min(groupsize), np.max(groupsize))
    for igroupsize in range(np.max(groupsize) + 1):
        itest = (groupsize == igroupsize)
        print('groups:', igroupsize, len(groupsize[itest]))

    # remove simple mirror pairs
    # for isource, source in enumerate(result):
    #    if


    key=raw_input("Enter any key to continue: ")

    id = np.linspace(1, nrows, num=nrows, dtype=int)
    print('id range:', np.min(id), np.max(id), len(id))
    # print('id:', len(result), len(id), np.min(id), np.max(id))

    id = Column(id, name='id')
    # result.add_column(id, index=0) # Insert before the first table column
    xmatch1.add_column(id, index=0)

    groupid = Column(groupid, name='groupid')
    # result.add_column(groupid, index=1)
    xmatch1.add_column(groupid, index=1)

    groupsize = Column(groupsize, name='groupsize')
    # result.add_column(groupsize, index=2)
    xmatch1.add_column(groupsize, index=2)

    xmatch1['dr_1_2'] = separation.arcsec
    xmatch1['PA_1_2'] = pa.degree
    xmatch1['dRA_1_2'] = dra.arcsec
    xmatch1['dDec_1_2'] = ddec.arcsec

    xmatch1.info('stats')
    print('Number of rows:', len(xmatch1))
    #result.info('stats')

    xmatch1.write('closepair_groups.fits', overwrite=True)
    # result.write('result_join.fits')

    key=raw_input("Enter any key to continue: ")

    idxmatch2_unique = np.unique(idxmatch2)
    print('Number of unique idxmatch1:', len(idxmatch1_unique))
    print('Number of unique idxmatch2:', len(idxmatch2_unique))

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
              np.min(dra.arcsec), np.max(dra.arcsec))
        print('dRA mean, std:',
              np.mean(dra.arcsec), np.std(dra.arcsec))
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

        ra2_xmatch = ra2[idxmatch2]
        dec2_xmatch = dec2[idxmatch2]

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

    separation = separation.arcsec
    dr = d2d.arcsec

    print(len(idxmatch1), len(idxmatch2), len(dr))

    return idxmatch1, idxmatch2, d2d.arcsec
