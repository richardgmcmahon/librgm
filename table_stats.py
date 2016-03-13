# $Source: /Users/rgm/soft/python/rgm/RCS/table_test.py,v $
# $Id: table_test.py,v 1.1 2009/08/18 11:09:42 rgm Exp rgm $     


def table_stats(data, ext=1, verbose=True, debug=False):
  """
  pyfits function to get information about a table

  USE:
  > python
  >>> from table_stats import *
  >>> help(table_stats)

  TODO:
  pyfits.info() for the object that has been read
  see pyfits(infile).info

  Original: Richard McMahon

  $Id: table_test.py,v 1.1 2009/08/18 11:09:42 rgm Exp rgm $     

  $Log: table_test.py,v $
  Revision 1.1  2009/08/18 11:09:42  rgm
  Initial revision

  Login name of author of last revision:   $Author: rgm $ 
  Date and time (UTC) of revision:         $Date: 2009/08/18 11:09:42 $
  Login name of user locking the revision: $Locker: rgm $ 
  CVS revision number:                     $Revision: 1.1 $ 
  """

  __version__ = "$Revision: 1.2 $"
  __date__ = "$Date: 2009/08/18 11:09:42 $"

  import sys
  import time

  import traceback

  import pyfits

  import numpy as np
  
  from pause import *

  print 'Executing: ',sys.argv[0], __version__

  if debug: help(data)

  #data, hdr = pyfits.getdata(infile, ext, header=True)

  infile=data

  if isinstance(data,np.ndarray): 
    print 'isInstance: numpy.ndarray'
    ncolumns=len(data.columns)
    nrows=len(data)
 
  print 'Infile: ', data
  print 'Extension: ', ext

  if not isinstance(data,np.ndarray): 
    print 'NOT isInstance: numpy.ndarray'
    hdr = pyfits.getheader(infile,ext)
    naxis2=hdr['naxis2']
    naxis1=hdr['naxis1']
    print 'naxis1: ',naxis1
    print 'naxis2: ',naxis2

    if naxis2 > 0:
      data = pyfits.open(infile)[ext].data
      if debug: help(data)

      header = pyfits.open(infile)[ext].header
      if debug: help(header)

      columns = pyfits.open(infile)[ext].columns
      if debug: help(columns)

      ncolumns = len(columns)

      print 'Number of columns: ', len(columns)
      print 'Number of rows: ',len(data)


  #help(data.columns.names)
  nrows=len(data)
  # : are used to identify empty strings from string variables

  for i in xrange(ncolumns):
      j=0
      # process the columns that are 1D vectors
      if len(data.field(i).shape) == 1:
        try:
          print i, j, data.columns[i].name, data.columns[i].format, \
           data.columns[i].dim, data.field(i).shape, len(data.field(i).shape), \
           len(data.field(i)), \
           ': ',np.min(data.field(i)), ' : ',np.max(data.field(i)) 
        except:
          # try min, max rather than np.min, np.max
          print i, j, data.columns[i].name, 'problem with column'
          print i, j, data.columns[i].name, data.columns[i].format, \
           data.columns[i].dim, data.field(i).shape, len(data.field(i).shape), \
           len(data.field(i)), \
           ': ', min(data.field(i)), ' : ', max(data.field(i)) 

          pass

      # process the columns that are 2D vectors (i,j)
      if len(data.field(i).shape) == 2:
        for j in xrange(data.field(i).shape[1]):
          print i,j, columns[i].name, columns[i].format, \
           columns[i].dim, data.field(i).shape, \
           len(data.field(i).shape), \
           len(data.field(i)), \
           ': ',np.min(data.field(i)[j]),' : ',np.max(data.field(i)[j])

  return
