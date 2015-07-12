from __future__ import print_function, division

def plotid(timestamp=True, user=True, hostname=False, progname=False,
 label=None, 
 top=False, right=False, verbose=False, debug=False):
  """ 
  Adds timestamp and other provenance information to a plot.

  Options:
  include date, username, hostname, program filename 
  
  could even geotag it?
  could add provenance to the png file
  
  Considerations: 

  should the text location be in units of the current figure (gcf)
  or the current axis (gca)

  see also https://github.com/matplotlib/matplotlib/issues/289

  options are not implemented yet
  text is placed on middle right in axis cords. 

  """



  import os
  import time
  import datetime
  import traceback

  import getpass
  import socket

  import matplotlib.pyplot as plt

  hostname_str=''
  if hostname: hostname_str = socket.gethostname()

  now = time.localtime(time.time())
  timestamp = time.strftime("%Y-%m-%dT%H:%M:%S",now)
  

  #print os.path.basename(trace[0]), ' line :', str(trace[1])
  #progname=os.path.basename(__file__)

  if debug:
    trace=traceback.print_exc()
    #help(trace)
    #print('len(trace): ', len(trace))
    trace = traceback.extract_stack()
    #help(trace)
    print('len(trace): ', len(trace))
    for each in trace:
      print(each)

  progname_str=''
  progline=''
  if progname:
    trace = traceback.extract_stack()[0]
    progname_str=os.path.basename(trace[0])
    progline=str(trace[1])
    progline='({})'.format(progline)
    
  if debug:
    print('progname: ', progname)
    print('progname_str: ', progname_str)
    print('progline: ', progline)

  #username=os.environ['USER'] 
  username = getpass.getuser()

  now = time.localtime(time.time())
  timestamp = time.strftime("%Y-%m-%dT%H:%M:%S",now)
  if debug or verbose: print('timestamp: ', timestamp)

  if label == None: label=''
  text = '{} {}{} {} {} {}'.format(label, 
   progname_str, progline,
   username, timestamp, hostname_str)

  #text = label+ ':  ' +timestamp+ ' ' +username
  #if host: text = text + '@'+hostname+']'

  if debug or verbose: print('text: ', text)

  # get current axis (gca)
  #ax=plt.gca()
  transform = plt.gca().transAxes
  #transform=plt.gcf().transFigure

  # this is needed to allow the text to be added before the first
  # axes are drawn
  #plt.setp(plt.gca(), xticks=(), yticks=())#, frame_on=False

  color='k'
  plt.figtext(0.97, 0.5, 
    text,
    transform=transform,
    rotation=90, 
    size='small', color=color,
    weight='ultralight',
    horizontalalignment='left', verticalalignment='center')

  return text

if __name__ == '__main__':

  import matplotlib.pyplot as plt

  plt.plot(range(10))

  plotid(debug=True, progname=True)

  plt.show()
