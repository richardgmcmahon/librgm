def plot_segmap(data=None, saveplot=True,
                plotfile_suffix=None, plotid=False):
    """

    plot colour segmentation map

    Original work from: VDESJ2325-5229_analysis.py

    """
    # determine the list of unique sources in the segmentation map image
    unique_sources = np.unique(data)
    nsources = len(unique_sources)
    print('Number of unique sources in the segmentation image: ', nsources)
    print(unique_sources)

    isource = 1
    # skip the first with value = zero which is background
    # replace the values of the image by a monotonic integer sequence
    # so that one can plot using a simple color lut
    # one could retain the values with a more fancy lut
    for unique_source in unique_sources[1:]:
        isource = isource + 1
        print(isource, unique_source)
        index = np.where(data == unique_source)
        print(index)
        data[index] = isource

    plt.figure(figsize=(8, 6))

    cmap = mpl.cm.jet
    # cmap = mpl.cm.jet_r
    # cmap.set_under(color='w')
    # cmax = np.max(data)
    # cmap.set_clim(1,cmax)
    # itest = data > 0.5
    # data[itest] = np.nan
    data = ma.masked_where(data < 0.5, data)
    cmap.set_bad('w')
    # plt.imshow(cutout.data, origin='lower', interpolation='nearest')
    plt.imshow(data, origin='lower', interpolation='nearest',
               cmap=cmap)

    if saveplot:
        plotfile = 'cutout'
        if segmap:
            plotfile = 'cutout_segmap'
        if weightmap:
            plotfile = 'cutout_weightmap'

        if plotfile_suffix is not None:
            plotfile = plotfile + '_' + plotfile_suffix

        if plotfile_prefix is not None:
            plotfile = plotfile_prefix + '_' + plotfile

        plotfile = plotfile + '.png'
        print('Saving :', plotfile)
        plt.savefig(plotfile)

    plt.show()

    return
