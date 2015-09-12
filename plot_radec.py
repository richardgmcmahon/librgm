
from matplotlib import pyplot as plt
from librgm.plotid import plotid

import numpy as np

def plot_radec(ra, dec, title=None, xlabel=None, ylabel=None,
  plotstyle=None, linestyle=None, markersize=None,
  rarange=None, decrange=None, showplots=False, figfile=None,
  figsize=(10.0,10.0), units=None, aspect=None, noplotid=False,
  plotdir='./', savefig=True, overplot=False):

  #plt.setp(lines, edgecolors='None')

  if figfile == None: figfile='radec.png'
  if not overplot: plt.figure(num=None, figsize=figsize)

  plt.xlabel('RA')
  if xlabel != None: plt.xlabel(xlabel)
  plt.ylabel('Dec')
  if ylabel != None: plt.ylabel(ylabel)
  if title != None: plt.title(title)

  xdata=ra
  ydata=dec

  print('RA range: ', np.min(xdata), np.max(xdata))
  print('Dec range: ', np.min(ydata), np.max(ydata))
  print('units: ', units)

  if rarange is None:
    plt.xlim([0,24.0])
  if rarange is not None:
    plt.xlim(rarange)

  if decrange is None:    
    plt.ylim([-90,30])
  if decrange is not None:    
    plt.ylim(decrange)

  if units == 'Degrees':
    print('units: ', units)
    plt.xlim([min(xdata),max(xdata)])
    plt.ylim([min(ydata),max(ydata)])

  if markersize is None: markersize=1.0
  if plotstyle is None:
    plt.plot(xdata, ydata, 'ob', markeredgecolor='b', markersize=markersize)

  if plotstyle is not None:
    print('plotstyle: ', plotstyle)
    plt.plot(xdata, ydata, plotstyle, 
     markeredgecolor=None, markersize=markersize)
  #plotid.plotid()

  ndata=len(xdata)
  print 'Number of data points plotted: ', ndata
  plt.legend([
   'n: '+ str(ndata)])
  plotid(progname=True)

  if aspect == 'equal':
    plt.axes().set_aspect('equal')

  if showplots: plt.show()

  if savefig: 
   print 'Saving: ', figfile
   plt.savefig(figfile)


