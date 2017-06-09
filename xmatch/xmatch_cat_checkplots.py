


def xmatch_cat_checkplots()


    import xmatch_checkplot
    import xmatch_checkplot0



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
