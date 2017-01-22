from __future__ import print_function, division

def tablemetadata(table=None, test=False):
  """
  add provenance metadata keywords to table

  At this time, the meta attribute of the Table class is simply an ordered
  dictionary and does not fully represent the structure of a FITS header
  (for example, keyword comments are dropped).

  Also, keywords are silently overwritten

  """


  import os
  import socket
  import getpass
  import time
  import datetime
  import traceback

  from astropy.table import Table

  hostname = socket.gethostname()
  username = getpass.getuser()

  trace = traceback.extract_stack()[0]
  progname=os.path.basename(trace[0])
  fullpath=trace[0]

  #ABSPATH=os.path.dirname(os.path.abspath(__file__))

  CWD=os.getcwd()

  timestamp=datetime.datetime.isoformat(datetime.datetime.now())


  if table is not None:

    table.meta['USERNAME']= username
    table.meta['HOSTNAME']= hostname
    table.meta['FULLPATH']= fullpath
    table.meta['PROGNAME']= progname
    table.meta['CWD']= CWD
    #table.meta['ABSPATH']= ABSPATH
    table.meta['TIME']= timestamp

  if test:

    a = [1, 4, 5]
    b = [2.0, 5.0, 8.2]
    c = ['x', 'y', 'z']
    table = Table([a, b, c], names=('a', 'b', 'c'),
     meta={'name': 'first table'})

    print('timestamp: ',datetime.datetime.isoformat(datetime.datetime.now()))

    now = time.localtime(time.time())
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S",now)

    table.meta['HISTORY']= 'Hello World'
    table.meta['HISTORY']= ['Hello World1','Hello World2']
    table.meta['COMMENT']= ['Hello World1','Hello World2']
    table.meta['USERNAME']= username
    table.meta['HOSTNAME']= hostname
    table.meta['PROGNAME']= progname
    table.meta['FULLPATH']= fullpath
    table.meta['TIME']= timestamp

    table.write('tmp.fits', overwrite=True)



if __name__ == "__main__":

  tablemetadata(test=True)
