"""


"""
def des_get_cutout(infile=None, data=None, ext=1, header=None,
               AstWCS=None,
               position=None, format='pixels', size=100,
               title=None, suptitle=None,
               imagetype='data',
               segmap=False, weightmap=False,
               plot=False, saveplot=True,
               plotfile_suffix=None, plotfile_prefix=None,
               verbose=False, debug=False):
    """



    """

    import numpy as np

    import matplotlib as mpl
    import matplotlib.pyplot as plt

    from astropy.nddata.utils import Cutout2D
    from astropy.io import fits
    from astropy import wcs
    from astropy.stats import mad_std
    from librgm.plotid import plotid


    print('position: ', position[0], position[1])
    position = np.rint(position)
    print('position: ', position[0], position[1])

    if infile is not None:
        hdulist = fits.open(infile)
        hdulist.info()
        AstWCS = wcs.WCS(hdulist[ext].header)
        xpix0 = np.rint(position[0]) - (size/2)
        ypix0 = np.rint(position[1]) - (size/2)
        xpix0 =  xpix0.astype(int)
        ypix0 =  ypix0.astype(int)
        print('xpix0, ypix0: ', xpix0, ypix0)
        xpix1 = xpix0 + size
        ypix1 = ypix0 + size
        data = hdulist[ext].data[ypix0:ypix1, xpix0:xpix1]

    if debug: help(data)
    print('data.shape: ', data.shape)
    median=np.median(data)
    print('median.shape: ', median.shape)
    print('median: ', median)

    if segmap:
        # determine the list of unique sources in the segmentation image
        unique_sources = np.unique(data)
        nsources = len(unique_sources)
        print('Number of unique segmented sources: ', nsources)
        print(unique_sources)
        isource = 1
        # skip the first with value = zero which is background
        for unique_source in unique_sources[1:]:
            isource = isource + 1
            print(isource, unique_source)
            index = np.where(data == unique_source)
            print(index)
            data[index] = isource

    if ext != 2:
        itest = data > 0.5
        print('min: ', np.min(data[itest]))
        threshold = np.min(data[itest]) - 1

        print('threshold: ', threshold)

    print('max: ', np.max(data))

    mad_stdev = mad_std(data)
    print('mad_std:', mad_stdev)

    if ext != 2:
        data = data - threshold
        itest = data < 0
        data[itest] = 0

    median=np.median(data)
    print('median: ', median)

    position = (size/2, size/2)
    cutout = Cutout2D(data, position, size)
    if debug: help(cutout)

    if plot:

        plt.figure(figsize=(8,6))

        cmap = mpl.cm.jet
        if segmap:
            #cmap = mpl.cm.jet_r
            #cmap.set_under(color='w')
            #cmax = np.max(data)
            #cmap.set_clim(1,cmax)
            #itest = data > 0.5
            #data[itest] = np.nan
            data = np.ma.masked_where(data < 0.5, data)
            cmap.set_bad('w')
        #plt.imshow(cutout.data, origin='lower', interpolation='nearest')
            plt.imshow(data, origin='lower', interpolation='nearest',
                cmap=cmap)

        if not segmap:
            crange = 50
            if weightmap:crange = 10
            lower = -1.0
            vmin = median + (lower * mad_stdev)
            vmax=  min([median+(crange*mad_stdev),max])
            plt.imshow(data, origin='lower', interpolation='nearest',
                cmap=cmap,
                vmin=vmin, vmax=vmax)

        plt.gca().invert_xaxis()

        plt.xlabel('pixels')
        plt.ylabel('pixels')
        if title is not None: plt.title(title)
        if suptitle is not None: plt.suptitle(suptitle)
        plt.colorbar()
        plotid()


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

    return cutout.data
