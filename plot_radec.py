
from matplotlib import pyplot as plt
from librgm.plotid import plotid

def plot_radec(ra, dec, title=None, xlabel=None, ylabel=None,
  rarange=None, decrange=None, showplots=False, figfile=None,
  figsize=(10.0,10.0), units=None, aspect=None, noplotid=False,
  plotdir='./'):

  #plt.setp(lines, edgecolors='None')

  if figfile == None: figfile='radec.png'

  plt.figure(num=None, figsize=figsize)

  plt.xlabel('RA')
  if xlabel != None: plt.xlabel(xlabel)
  plt.ylabel('Dec')
  if ylabel != None: plt.ylabel(ylabel)
  if title != None: plt.title(title)

  ms=1.0

  xdata=ra
  ydata=dec


  print('RA range: ', min(xdata), max(xdata))
  print('Dec range: ', min(ydata), max(ydata))
  print('units: ', units)

  if rarange is None:
    plt.xlim([0,24.0])

  if decrange is None:    
    plt.ylim([-90,30])

  if units == 'Degrees':
    print('units: ', units)
    plt.xlim([min(xdata),max(xdata)])
    plt.ylim([min(ydata),max(ydata)])

  ms=1.0
  plt.plot(xdata, ydata, 'ob', markeredgecolor='b', ms=ms)
  #plotid.plotid()

  ndata=len(xdata)
  print 'Number of data points plotted: ', ndata
  plt.legend([
   'n: '+ str(ndata)])
  plotid(progname=True)

  if aspect == 'equal':
    plt.axes().set_aspect('equal')

  if showplots: plt.show()

  print 'Saving: ', figfile
  plt.savefig(figfile)


