# librgm

Mainly utility functions


to use either clone or download or fork and clone

To use you do not need to install into PYTHONPATH. I use
via this method for development convenience. I probably break
some rules. The code is designed for use by local people 
and hence access via path is used.


To make your own put all your code in a directory tree and
put an empty __init__.py in the directory as shown.

sys.path.append('/home/rgm/soft/python/lib/')

# not sure how this is used for
import librgm as rgm


# single function call table_index_column with usage
# icol=table_index_column()
from librgm.table_index_column import table_index_column

# single function with usage plotid(progname=progname)
from librgm.plotid import plotid

# single function with usage table_stats(infile=infile)
from librgm.table_stats import table_stats

# group of functions with usage new=vega2ab.wise()
from librgm.vega2ab import *

# usage
help(rgm)
plotid
table_stats()


