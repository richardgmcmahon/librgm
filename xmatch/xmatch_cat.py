def xmatch_2cats(data1=None, data2=None,
                 colnames_radec1=['ra', 'dec'],
                 colnames_radec2=['ra', 'dec'],
                 units_radec1=['degree', 'degree'],
                 units_radec2=['degree', 'degree'],
                 plotfile_label="",
                 rmax=30.0,
                 nthneighbor=1,
                 **kwargs):
    """RA, Dec xmatch for two lists; returns pointers


    """

    print('colnames_radec1:', colnames_radec1)
    print('colnames_radec2:', colnames_radec2)
    print('plotfile_label:', plotfile_label)

    # print(data1[0])
    # print(data2[0])

    ra1 = data1[colnames_radec1[0]]
    dec1 = data1[colnames_radec1[1]]

    ra2 = data2[colnames_radec2[0]]
    dec2 = data2[colnames_radec2[1]]

    skycoord_object1 = SkyCoord(ra1, dec1, unit=units_radec1, frame='icrs')
    skycoord_object2 = SkyCoord(ra2, dec2, unit=units_radec1, frame='icrs')

    # idx is an integer array into the first cordinate array to get the
    # matched points for the second coorindate array.
    # Shape of idx matches the first coordinate array
    idx, d2d, d3d = match_coordinates_sky(skycoord_object1,
                                          skycoord_object2,
                                          nthneighbor=nthneighbor)



    ra2_xmatch = ra2[idx]
    dec2_xmatch = dec2[idx]

    sep = skycoord_object1.separation(skycoord_object2[idx])
    median_separation = np.median(sep).arcsec
    print('Median separation (arc seconds):', median_separation)

    suptitle = plotfile_label
    plotfile = 'plot_xmatch_' + plotfile_label + 'a_checkplot.png'

    xmatch_checkplot(ra1, dec1, ra2_xmatch, dec2_xmatch,
                     width=rmax,
                     gtype='square',
                     saveplot=True,
                     plotfile=plotfile,
                     suptitle=suptitle)
    plt.close()

    plotfile = 'plot_xmatch_' + plotfile_label + '_b_checkplot0.png'
    xmatch_checkplot0(ra1, dec1, ra2_xmatch, dec2_xmatch,
                      width=10.0,
                      gtype='square',
                      saveplot=True,
                      plotfile=plotfile,
                      suptitle=suptitle)

    idx1 = idx
    idx2 = []
    sep = []

    return idx1, idx2, sep
