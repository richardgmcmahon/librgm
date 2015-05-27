
from matplotlib import pyplot as plt

def plot_radec(ra, dec, title=None, xlabel=None, ylabel=None,
  rarange=None, decrange=None, showplots=False, figfile=None,
  figsize=(10.0,10.0),
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


  print min(xdata), max(xdata)
  print min(ydata), max(ydata)

  if rarange is None:
    plt.xlim([0,24.0])

  if decrange is None:    
    plt.ylim([-90,30])

  ms=1.0
  plt.plot(xdata, ydata, 'ob', markeredgecolor='b', ms=ms)
  #plotid.plotid()

  ndata=len(xdata)
  print 'Number of data points plotted: ', ndata
  plt.legend([
   'n: '+ str(ndata)])

  if showplots: plt.show()

  print 'Saving: ', figfile
  plt.savefig(figfile)


