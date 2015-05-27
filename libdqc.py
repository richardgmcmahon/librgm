from __future__ import print_function, division

__version__="v0.0.1"

"""

 Library of Python function used for QC analysis of imaging surveys.

 Initially developed in IDL for INT WFC survey, further developments
 for UKIDSS LAS survey; VISTA Hemisphere survey. 

 TODO:

 get filtername from VSA query and ESO program ID


"""

import os
import sys
import time
import traceback
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import numpy as np

from scipy import stats 

import astroML.stats as aml

import astropy
from astropy import coordinates as coord
from astropy import units as u

#from astropy.coordinates import ICRSCoordinates
# converting from pre0.4 to 1.0
from astropy.coordinates import SkyCoord

from astropy.io import ascii

#import pyfits as pyfits
from astropy.io import fits as pyfits

from table_stats import *

now = time.localtime(time.time())
print('Current time: ',time.strftime("%Y-%m-%d %H:%M:%S %Z", now))
date=time.strftime("%Y%m%d", now)
print('day: ',date)
print('Current working directory: ',os.getcwd())
print( 'Executing: ',sys.argv[0])

now = time.localtime(time.time())
timestamp = time.strftime("%Y-%m-%dT%H:%M:%S",now)
datestamp = time.strftime("%Y%m%d",now)

print('timestamp: ', timestamp)
print('datestamp: ', datestamp)


def mymad(data, median=None, sigma=False):
  """
  compute median absolute deviation
  Options: 
    provide precomputed median
    return the equivalenet sigma
    maybe offer variance too
  """
  if median is None: median=np.median(data)

  mad=np.median (abs(data-median))

  if sigma: mad=mad/0.6745

  return mad


def mypercentile(a, q, index, debug=False, verbose=False):
  """
  Efficient calculation of percentiles using a sorted array. The sorting
  is an overhead but if you need more than 4 percentiles including the
  median, it is more efficient.

  For consistency a, q are the variables used in numpy.percentile
  index is the sort order produced using numpy.argsort
  e.g. index=np.argsort(data, axis=None)
 
  may need to modified to deal with the not integer indices 


  """

  ndata=a.size
  step_pc=ndata/100.0
  ipc=q
  # trap the 
  ipoint_pc=min(ipc*step_pc, ndata-1)

  if debug: print('mypercentile: ', q, ipoint_pc, int(ipoint_pc), index[int(ipoint_pc)])
  result=a.flat[min(index[int(ipoint_pc)], ndata-1)]
  if verbose: print('mypercentile: ', q, result)

  return result

def mymad2(data):
  median=np.median(data)
  return np.median (abs(data-median))

#def imstats(data):

  


def rd_dqc(infile=None, debug=None):
  """
   read the dqc file

  """
  
  print('dqc: ', infile)
  if not os.path.exists(infile): 
    print(infile, 'does not exist')
    print('Exiting')
    sys.exit(0)

  # open catalogue file handle
  fh = pyfits.open(infile)
  data = fh[1].data
  print('Number of rows: ', len(data))
  #help(data)

  if debug: table_stats(infile)

  #data['ra']=np.degrees(data['ra'])
  #data['dec']=np.degrees(data['dec'])

  return data

def get_filenames(dqc=None, debug=True):
  """
  Get a list of all the unique tile images used
  """
  filenames=[dqc['Yfilename'],dqc['Jfilename'],
   dqc['Hfilename'],dqc['Ksfilename']]
  print('Filenames: ', len(filenames))
  #mjdobs=flatten(mjdobs)
  #help(mjdobs)
  filenames=np.array(filenames)
  print('Number: ', len(filenames))
  
  filenames=filenames.flatten()
  print('Number: ', len(filenames))
  print(filenames.shape)
  print(filenames.size)
  print('dtype: ', filenames.dtype)

  mask= np.char.strip(filenames) != 'NONE'
  print('Number: ', len(mask))
  
  print('Number: ', len(filenames[mask]))

  filename_start=min(filenames[mask])
  filename_end=max(filenames[mask])

  print(filename_start, ' -> ',filename_end)

  return filenames


def duplicate_tiles():
  """
  find duplicate tiles 

  method:

  make unique list
  or
  sort and then trawl through

  """

  unique, unique_indices, original_indices =  np.unique(data, return_indices=True, return_inverse=True)


def plot_radec(ra, dec, title=None, xlabel=None, ylabel=None,
  rarange=None, decrange=None, showplots=False, figfile=None):

  #plt.setp(lines, edgecolors='None')

  if figfile == None: figfile='radec.png'

  ax=plt.figure(num=None, figsize=(10.0, 10.0))

  plt.xlabel('RA')
  if xlabel != None: plt.xlabel(xlabel)
  plt.ylabel('Dec')
  if ylabel != None: plt.ylabel(ylabel)
  if title != None: plt.title(title)

  ms=1.0

  xdata=ra
  ydata=dec


  print(min(xdata), max(xdata))
  print(min(ydata), max(ydata))

  #plt.xlim([0,360])
  #plt.ylim([-90,30])

  ms=1.0
  plt.plot(xdata, ydata, 'ob', markeredgecolor='b', ms=ms)
  #plotid.plotid()

  ndata=len(xdata)
  print('Number of data points plotted: ', ndata)
  plt.legend([
   'n: '+ str(ndata)])

  if showplots: plt.show()

  print('Saving: ', figfile)
  plt.savefig(figfile)


def plot_band(data=None, colname=None, color=None, 
 normpdf=False, xlimit_min=None, xlimit_max=None, xscale=None,
 xlabel=None, filename=None):

  global t0

  if color == None: color='k'

  # determine cumulative frequency distribution by sorting values
  # this is faster than the percentile function
  ndata=len(data)
  index=np.argsort(data, axis=None)
  median=data[index[int(ndata/2.0)]]
  sigma_mad=mymad(data, median=median, sigma=True)
  min=data[index[0]]
  max=data[index[-1]]

  ndata, (dmin, dmax), mean, variance, skewness, kurtosis = \
         stats.describe(data, axis=None)

  sigma=math.sqrt(variance)


  print('min, max, mean, sigma, median, sigma_mad: ')
  print(min, max, mean, sigma, median, sigma_mad)
  sigmaIQ=aml.sigmaG(data)
  print('sigmaIQ: ', aml.sigmaG(data))
  print('Elapsed time(secs): ',time.time() - t0)

  q10, q90 = np.percentile(data, [10.0, 90.0])
  sigma80= (q90-q10) * 0.5000* 0.7803
  print(q10, q90)
  print('sigma80: ', sigma80)

  q25, q50, q75 = np.percentile(data, [25.0, 50.0, 75.0])
  print(q25, q50, q75)

  step_pc=ndata/100.0
  ipc=50.0
  ipoint_pc=ipc*step_pc
  print('median: ', int(ipoint_pc), index[int(ipoint_pc)])
  print('median: ', data[index[int(ipoint_pc)]])
  print('Elapsed time(secs): ',time.time() - t0)
  
  range=np.linspace(0.0,100.0,101)
  #print 'range: ', range
  
  dist=np.zeros(101)
  i=-1
  for pc in range:
    i=i+1
    dist[i]=mypercentile(data, pc, index, verbose=True, debug=False)
  print('Elapsed time(secs): ',time.time() - t0)
    
  plotcdf=True
  if plotcdf:
    xdata=dist
    ydata=range/100.0
    #title=filename + '[' + str(ext) + ']'
    title=filename
    ylabel='Cumulative frequency'

    plt.plot(xdata, ydata, color=color, markersize=1,
     linestyle='-', linewidth=2)
    if xlimit_min == None: xlimit_min=median-(5.0*sigma_mad)
    if xlimit_max == None: xlimit_max=median+(5.0*sigma_mad)

    ax=plt.figtext(0.7, 0.4, 'plt.figtext: Hello World')
  
    print('Default font size ', ax.get_size())
    #ax.set_size(ax.get_size()*2.0)
    #print('Default font size ', ax.get_size())


    #plt.figtext(0.5, 0.5, 'Font size: ' + str(plt.get_size()))

    plt.xlim([xlimit_min, xlimit_max])
    if xscale: plt.xscale('log')

    plt.title(title)
    if xlabel != None: plt.xlabel(xlabel)
    plt.ylabel(ylabel)


    #plt.tick_params(axis='both', which='major', labelsize=10)
    #plt.tick_params(axis='both', which='minor', labelsize=8)

    #plt.xlim(plot_xlimits)

    # Compute the CDF; need to check that cdf is not off by one step via
    # reversing the cdf by hand to a pdf, by eye I see an offset when the 
    # nsteps=100 but it is not visible for nsteps=1000 so it looks like the
    # pdf and/or cdf is shofted by 1 step 
    if normpdf:
      nsteps=1000
      xmin=median-(5.0*sigma_mad)
      xmax=median+(5.0*sigma_mad)
      xrange=10.0*sigma_mad
      # use nsteps+1 so that there is a value at the midpt
      x = np.linspace(xmin,xmax,nsteps+1)

      pdf=mlab.normpdf(x,median,sigma_mad)

      dx=xrange/nsteps
      cdf = np.cumsum(pdf*dx)
      plt.plot(x,cdf)

      pdf=mlab.normpdf(x,median,sigmaIQ)
      dx=xrange/nsteps
      cdf = np.cumsum(pdf*dx)
      plt.plot(x,cdf,color='green')

      pdf=mlab.normpdf(x,median,sigma80)
      dx=xrange/nsteps
      cdf = np.cumsum(pdf*dx)
      plt.plot(x,cdf,color='red')

def plot_byband(data=None, 
 wavebands=None, colparam=None,
 xlabel=None, masklimit=None, xlimit_min=None, xlimit_max=None, xscale=None,
 cdf=True, pdf=False, normpdf=False,   
 showplots=False, filename=None, plotdir='./'):

  """
  Plots cumulative distributions of parameters with wavebands overplotted  

  """

  global t0

  t0=time.time()

  # if isinstance(filename,str):


  fig = plt.figure(num=None, figsize=(10.0, 10.0))
  ax = fig.add_subplot(1,1,1) 



  if wavebands == None: print('Number of wavebands: ', 'None')
  if wavebands != None: 
    print('Number of wavebands: ', len(wavebands))
    for waveband in wavebands:
      print('Waveband: ', waveband)

  i=-1
  colors=['b','g','DarkOrange','r']
  textstr=''
  for waveband in wavebands:
    i=i+1
    colname= str(waveband) + str(colparam)
    pdata=data[colname]
    if masklimit != None: pdata=pdata[pdata > masklimit]
    color=colors[i]
    plot_band(data=pdata, colname=colname, xlabel=xlabel, 
     filename=filename, color=color, 
     xlimit_min=xlimit_min, xlimit_max=xlimit_max, xscale=xscale)

    q10, q50, q90 = np.percentile(pdata, [10.0, 50.0, 90.0])
    textstr = textstr + '%-4s %s %s %s %s\n' %(waveband, str(len(pdata)), str(q50), str(q10), str(q90))

  for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    print(str(item) + ': ', item.get_fontsize())
    item.set_fontsize(item.get_fontsize()*1.2)

  # strip off final linefeed
  textstr=textstr[:-1]

  # these are matplotlib.patch.Patch properties
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  # place a text box in upper left in axes coords
  ax.text(0.50, 0.15, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props, family='monospace')
  #prop={'family': 'monospace'})

  #plt.legend(legends, loc=1, prop={'family': 'monospace'})
  ax.legend(loc=1, prop={'family': 'monospace'})

  basename=os.path.basename(filename)
  ext=""
  plt.savefig(basename + '_' + str(ext) + colname+ '_cdf.png')


  
  if showplots: plt.show()

  plt.close()

def plot_cdf(data=None,
 showplots=False, filename="", 
 xlabel=None, plotlabel=""):
  
  t0=time.time()

  ax=plt.figure(num=None, figsize=(10.0, 10.0))

  # determine cumulative frequency distribution by sorting values
  # this is faster than the percentile function
  ndata=len(data)
  index=np.argsort(data, axis=None)
  median=data[index[int(ndata/2.0)]]
  sigma_mad=mymad(data, median=median, sigma=True)
  min=data[index[0]]
  max=data[index[-1]]

  ndata, (dmin, dmax), mean, variance, skewness, kurtosis = \
         stats.describe(data, axis=None)

  sigma=math.sqrt(variance)


  print('min, max, mean, sigma, median, sigma_mad: ')
  print(min, max, mean, sigma, median, sigma_mad)
  sigmaIQ=aml.sigmaG(data)
  print('sigmaIQ: ', aml.sigmaG(data))
  print('Elapsed time(secs): ',time.time() - t0)

  q10, q90 = np.percentile(data, [10.0, 90.0])
  sigma80= (q90-q10) * 0.5000* 0.7803
  print(q10, q90)
  print('sigma80: ', sigma80)

  q25, q50, q75 = np.percentile(data, [25.0, 50.0, 75.0])
  print(q25, q50, q75)

  step_pc=ndata/100.0
  ipc=50.0
  ipoint_pc=ipc*step_pc
  print('median: ', int(ipoint_pc), index[int(ipoint_pc)])
  print('median: ', data[index[int(ipoint_pc)]])
  print('Elapsed time(secs): ',time.time() - t0)
  
  range=np.linspace(0.0,100.0,101)
  #print 'range: ', range
  
  dist=np.zeros(101)
  i=-1
  for pc in range:
    i=i+1
    dist[i]=mypercentile(data, pc, index, verbose=True, debug=False)
  print('Elapsed time(secs): ',time.time() - t0)
    
  plotcdf=True
  if plotcdf:
    xdata=dist
    ydata=range/100.0
    #title=filename + '[' + str(ext) + ']'
    title=filename + ': ' + plotlabel
    ylabel='Cumulative frequency'

    plt.plot(xdata, ydata, 'k', color='black', markersize=1)
    plt.xlim([median-(5.0*sigma_mad),median+(5.0*sigma_mad)])
    plt.title(title)
    if xlabel != None: plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Compute the CDF; need to check that cdf is not off by one step via
    # reversing the cdf by hand to a pdf, by eye I see an offset when the 
    # nsteps=100 but it is not visible for nsteps=1000 so it looks like the
    # pdf and/or cdf is shofted by 1 step 
    nsteps=1000
    xmin=median-(5.0*sigma_mad)
    xmax=median+(5.0*sigma_mad)
    xrange=10.0*sigma_mad
    # use nsteps+1 so that there is a value at the midpt
    x = np.linspace(xmin,xmax,nsteps+1)

    pdf=mlab.normpdf(x,median,sigma_mad)

    dx=xrange/nsteps
    cdf = np.cumsum(pdf*dx)
    plt.plot(x,cdf)

    pdf=mlab.normpdf(x,median,sigmaIQ)
    dx=xrange/nsteps
    cdf = np.cumsum(pdf*dx)
    plt.plot(x,cdf,color='green')

    pdf=mlab.normpdf(x,median,sigma80)
    dx=xrange/nsteps
    cdf = np.cumsum(pdf*dx)
    plt.plot(x,cdf,color='red')

    basename=os.path.basename(filename)
    ext=""
    plt.savefig(basename + '_' + str(ext) + plotlabel + '_cdf.png')

    if showplots: plt.show()

    plt.close()


def get_maglimit(data=None, waveband=None, casu=True, Dye2006=False):
  """
  Compute the point source magnitude limit

  might need to check that zeropoint is at the observation airmass or
  at the zenith see casucat.maglim

  not sure how aperture radius is determined
  cfactor?

  """
  pi=3.141593

  nsigma=5.0
  cfactor=1.2

  photzpcat=data[waveband+'photzpcat']
  exptime=data[waveband+'exptime']
  skynoise=data[waveband+'skynoise']
  apercor3=data[waveband+'apercor3']
  pixsize=data[waveband+'xpixsize']

  maglimit=photzpcat-2.5*np.log10(nsigma*skynoise*np.sqrt(cfactor*pi)/(pixsize*exptime))-apercor3

  return maglimit





