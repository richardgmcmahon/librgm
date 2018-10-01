
import matplotlib.pyplot as plt
import numpy as np

from librgm.plotid import plotid

def plot_histogram(data,
                   max_data=None,
                   range=None,
                   bins='knuth',
                   figsize=(6,6),
                   xlabel=None, ylabel=None,
                   label=None,
                   suptitle=None,
                   plotfile_prefix=None,
                   plotfile_suffix=None,
                   plotfile=None,
                   outpath=None,
                   showplot=None,
                   saveplot=True):
    """
    plot a histogram using astropy.visualization.hist
    UPDATE: was ported from astroML.plotting.hist (http://astroML.org/)

    *astropy.visualization.hist*

    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html

    astropy.visualization.hist(x, bins=10, ax=None, **kwargs)

    http://docs.astropy.org/en/stable/api/astropy.visualization.hist.html
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html

    Enhanced histogram function

    This is a histogram function that enables the use of more sophisticated
    algorithms for determining bins. Aside from the bins argument allowing a
    string specified how bins are computed, the parameters are the same as
    pylab.hist().

    matplotlib.pyplot.hist(x, bins=None,
                           range=None, density=None, weights=None,
                           cumulative=False, bottom=None,
                           histtype='bar', align='mid',
                           orientation='vertical', rwidth=None,
                           log=False, color=None, label=None,
                           stacked=False, normed=None,
                           hold=None, data=None,
                           **kwargs)



    http://www.astroml.org/modules/generated/astroML.plotting.hist.html

    astroML.plotting.hist(x, bins=10, range=None, ax=None, **kwargs)

    Enhanced histogram

    bins : int or list or str (optional)

    If bins is a string, then it must be one of:
    'blocks' : use bayesian blocks for dynamic bin widths
    'knuth' : use Knuth's rule to determine bins
    'scott' : use Scott's rule to determine bins
    'freedman' : use the Freedman-diaconis rule to determine bins

    This is a histogram function that enables the use of more sophisticated
    algorithms for determining bins. Aside from the bins argument allowing
    a string specified how bins are computed, the parameters are the same
    as pylab.hist().



    """
    # from astroML.plotting import hist
    from astropy.visualization import hist

    if max_data != None:
        max_data = np.max(dist)
    xmax = max_data

    fig = plt.figure(figsize=figsize)
    # fig = plt.gcf()
    # fig.set_size_inches(10,10)

    ax = plt.axes()
    ndata = len(data)
    if range is None:
        range = [np.min(data), np.max(data)]
    if range is not None:
        print('range:', range, np.min(data), np.max(data))
        print(range, type(data), type(range), type(range[0]))
        print(data.dtype)
        idata = (data > range[0])
        # & data < range[1])
        print(len(data), len(data[idata]))
        data = data[idata]
    ndata = len(data)
    print('bins:', bins)
    hist(data, bins=bins, range=range,
         ax=ax, label=str(ndata),
         histtype='stepfilled',
         ec='k', fc='#AAAAAA')

    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is None: ax.set_ylabel('counts')
    if ylabel is not None: ax.set_ylabel(ylabel)

    if suptitle is not None:
        plt.suptitle(suptitle, fontsize='medium')

    #plt.show()

    # get basename without file extension
    #basename=os.path.splitext(os.path.basename(filename))[0]
    #figname = basename + '_' + 'scheme3_image_sep_NN_360arcsec_arcmin.png'

    plt.legend()
    plotid()

    if saveplot:
        if plotfile is None and plotfile_suffix is None:
            plotfile = 'histogram.png'
        if plotfile is None and plotfile_suffix is not None:
            plotfile = 'histogram_' + plotfile_suffix + '.png'

        if outpath is None:
            outpath = './'
        print('plotfile:', plotfile)
        print('outpath:', outpath)
        plotfile = outpath + plotfile
        print('Saving:', plotfile)
        plt.savefig(plotfile)

    if showplot:
        plt.show()

    plt.close()

    return
