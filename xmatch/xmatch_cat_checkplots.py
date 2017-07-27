def xmatch_cat_checkplots(table1=None, table2=None, idxmatch=None,
                          colnames_radec1=['ra', 'dec'],
                          colnames_radec2=['ra', 'dec'],
                          units_radec1=['degree', 'degree'],
                          units_radec2=['degree', 'degree'],
                          rmax=10.0, rmax2=None,
                          debug=False,
                          verbose=False)

    import xmatch_checkplot
    import xmatch_checkplot0

    ra1 = table1[colnames_radec1[0]]
    dec1 = table1[colnames_radec1[1]]

    ra2 = table2[colnames_radec2[0]]
    dec2 = table2[colnames_radec2[1]]

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
