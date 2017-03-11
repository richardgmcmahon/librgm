from __future__ import print_function, division

def mk_ps1_url(RA, DEC, size=None, output_size=None, zoom_factor=1.0):
    """

    Default:

    60"x60" default
    ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=153.93341,12.45196

    zoomx2
    30"x30"
    ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=153.93341,12.45196&size=120&output_size=256

    zoomx4
    15"x15"
    http://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=153.93341,12.45196&size=60&output_size=256

    size = 60.0/zoom_factor


    http://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=07%3A16%3A03.58++%2B47%3A08%3A50.0&filter=color&filter=g&filter=r&filter=i&filter=z&filter=y&filetypes=stack&auxiliary=data&size=1024&output_size=0&verbose=0&autoscale=99.500000&catlist=

    """
    url_tail = "filter=color&filter=g&filter=r&filter=i&filter=z&filter=y&filetypes=stack&auxiliary=data&size=1024&output_size=0&verbose=0&autoscale=99.500000&catlist="

    url_base = 'http://ps1images.stsci.edu/cgi-bin/ps1cutouts?'

    if output_size is None:
        output_size = 128

    if size is None:
        size = int(60.0/zoom_factor)

    url = "<A HREF = " + url_base + \
       "pos=" + str("%.5f" % RA) + "," + str("%.5f" % DEC) + \
       "&size=" + str("%.0f" % size) + \
       "&output_size=" + str("%.0f" % output_size) +\
       "> PS1_DR1 </A>"

    return url
