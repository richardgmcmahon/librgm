
from matplotlib import pyplot as plt
from librgm.plotid import plotid

import numpy as np

def plot_radec(ra, dec,
               figsize=(8.0, 8.0),
               title=None, suptitle=None,
               xlabel=None, ylabel=None, plotlabel='',
               plotstyle=None, linestyle=None,
               markersize=None,
               marker='+', color='b',
               rarange=None, decrange=None,
               showplots=False,
               plotfile=None,
               plotfile_prefix=None,
               plotfile_suffix=None,

               units=None, aspect=None, noplotid=False,
               nolegend=False, verbose=False,
               plotdir='./', savefig=True, overplot=False):

    #plt.setp(lines, edgecolors='None')

    if plotfile == None: plotfile='radec.png'
    if not overplot: plt.figure(num=None, figsize=figsize)

    plt.xlabel('RA')
    if xlabel != None: plt.xlabel(xlabel)
    plt.ylabel('Dec')
    if ylabel != None: plt.ylabel(ylabel)
    if title != None: plt.title(title)
    if suptitle != None: plt.suptitle(suptitle)

    xdata=ra
    ydata=dec

    if verbose: print('RA range: ', np.min(xdata), np.max(xdata))
    if verbose: print('Dec range: ', np.min(ydata), np.max(ydata))
    if verbose: print('units: ', units)

    if rarange is None:
        plt.xlim([min(xdata),max(xdata)])
    if rarange is not None:
        plt.xlim(rarange)

    if decrange is None:
        plt.ylim([min(ydata),max(ydata)])
    if decrange is not None:
        plt.ylim(decrange)


    if markersize is None:
        markersize=1.0

    ndata=len(xdata)

    if plotstyle is None:
        plt.plot(xdata, ydata,
                 marker='o', c=color,
                 linestyle='None',
                 markeredgecolor=color,
                 markersize=markersize,
                 label=plotlabel + str(ndata))

    if plotstyle is not None:
      if verbose: print('plotstyle: ', plotstyle)
      plt.plot(xdata, ydata, plotstyle,
       markeredgecolor=None, markersize=markersize)
    #plotid.plotid()


    if verbose:
        print 'Number of data points plotted: ', ndata

    if not nolegend:
        plt.legend()

    plt.grid()

    if not noplotid:
        plotid(progname=True)

    if aspect == 'equal':
        plt.axes().set_aspect('equal')

    if showplots:
        plt.show()

    if savefig:
        print 'Saving: ', plotfile
        plt.savefig(plotfile)
