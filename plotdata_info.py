# Python 2/3 compatability
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# add support for raw_input to Python 3
from builtins import input
try:
   input = raw_input
except NameError:
   pass

def plotdata_info(xdata=None, ydata=None,
                  xrange=None, yrange=None,
                  verbose=True):
    """
    xdata is required for univariate analysis such as a histogram

    xdata and ydata are required for bivariate analysis like a scatter plot

    """
    import numpy as np

    if xdata is None:
       print('Returning since xdata=None')
       return

    # create Dict to store the info
    info = {}

    ndata = len(xdata)
    info['ndata_all'] = ndata
    info['ndata'] = ndata
    info['nxdata'] = ndata

    if ydata is not None:
       info['nydata'] = len(ydata)

    # x-axis data
    print('xrange:', xrange)

    # get full range of xdata
    xdata_min = np.min(xdata)
    xdata_max = np.max(xdata)
    info['xdata_range'] = [xdata_min, xdata_max]

    # get full range excluding NANs
    xdata_min_notnan = np.nanmin(xdata)
    xdata_max_notnan = np.nanmax(xdata)
    info['xdata_min_notnan'] = xdata_min_notnan
    info['xdata_max_notnan'] = xdata_max_notnan
    # some convenience redundancy
    info['xdata_range_notnan'] = [xdata_min_notnan,
                                  xdata_max_notnan]

    # count the NANs
    info['ndata_xnan'] = np.isnan(xdata).sum()
    # count the INFs
    info['ndata_xinf'] = np.isinf(xdata).sum()


    # y-axis data
    if ydata is not None:
        print('yrange:', yrange)

        if yrange is not None:
            iydata = (ydata > yrange[0]) & (ydata < yrange[1])
            nydata = len(ydata[iydata])

        ydata_min = np.min(ydata)
        ydata_max = np.max(ydata)
        info['ydata_range'] = [xdata_min, xdata_max]

        ydata_min_notnan = np.nanmin(ydata)
        ydata_max_notnan = np.nanmax(ydata)
        info['ydata_range_notnan'] = [ydata_min_notnan,
                                     ydata_max_notnan]

        info['ndata_ynan'] = np.isnan(ydata).sum()
        info['ndata_yinf'] = np.isinf(ydata).sum()

        ixydata_nan = (np.isnan(xdata) & np.isnan(ydata))
        ixydata_inf = (np.isinf(xdata) & np.isinf(ydata))
        ndata_xynan = len(xdata[ixydata_nan])
        ndata_xyinf = len(xdata[ixydata_inf])
        info['ndata_xynan'] = ndata_xynan
        info['ndata_xyinf'] = ndata_xyinf

        # limit xdata to the xrange
        if yrange is not None:
            iydata = (ydata > yrange[0]) & (ydata < yrange[1])
            nydata = len(ydata[iydata])
            info['nydata'] = nydata
            # ydata = ydata[iydata]

        if xrange and yrange is not None:
            idata = (xdata > xrange[0]) & (xdata < xrange[1]) & \
                    (ydata > yrange[0]) & (ydata < yrange[1])
            info['ndata'] = len(xdata[idata])

    # limit xdata to the xrange
    if xrange is not None:
        ixdata = (xdata > xrange[0]) & (xdata < xrange[1])
        nxdata = len(xdata[ixdata])
        info['nxdata'] = nxdata

    if xrange is not None and ydata is None:
        xdata = xdata[ixdata]

    if xrange and yrange is not None:
       xdata = xdata[idata]
       ydata = ydata[idata]

    if verbose:
       xlabel = 'x-axis'
       print()
       print(xlabel)
       print(xlabel + ' range:',
             info['xdata_range'][0], info['xdata_range'][1],
             info['ndata'])
       print(xlabel + ' range (excluding NaNs):',
             info['xdata_range_notnan'][0],
             info['xdata_range_notnan'][1])
       print(xlabel + ' (nan):', info['ndata_xnan'])
       print(xlabel + ' (inf):', info['ndata_xinf'])

    if verbose and ydata is not None:
       ylabel = 'y-axis'
       print()
       print(xlabel)
       print(xlabel + ' range:',
             info['ydata_range'][0], info['ydata_range'][1],
             info['ndata'])
       print(xlabel + ' range (excluding NaNs):',
             info['ydata_range_notnan'][0],
             info['ydata_range_notnan'][1])
       print(xlabel + ' (nan):', info['ndata_ynan'])
       print(xlabel + ' (inf):', info['ndata_yinf'])

    label = 'xy in range; ' + str(info['ndata']) + ' out of: ' + \
         str(info['ndata_all']) + '\n' + \
         'x, y in range; ' + str(info['nxdata']) + ': ' + \
         str(info['nydata']) + '\n' + \
         'x range (full); ' + \
         str(info['xdata_range_notnan'][0]) + ': ' + \
         str(info['xdata_range_notnan'][1]) + '\n' + \
         'y range (full); ' + \
         str(info['ydata_range_notnan'][0]) + ': ' + \
         str(ydata_max_notnan) + '\n' + \
         'x, y, xy (nan); ' + \
         str(info['ndata_xnan']) + ': ' + str(info['ndata_ynan']) + ': ' + \
         str(info['ndata_xynan']) + '\n' + \
         'x, y (inf); ' + \
         str(info['ndata_xinf']) + ': ' + str(info['ndata_yinf']) + ': ' + \
         str(info['ndata_xyinf'])

    return info, label
