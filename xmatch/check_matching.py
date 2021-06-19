from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


"""

orginal from Chris Desira
I have replaced pylab by plt
See also:  /Users/rgm/soft/python/xmatch/check_matching.py

fixed bins issue; needs to be int in hist

"""

# standard libraries
import inspect
import os
import sys
import time

try:
    # Python 2
    from itertools import izip
except ImportError:
     # Python 3
     izip = zip


# 3rd party libraries
import numpy as np

#import fitsio

from astropy.coordinates import (search_around_sky, SkyCoord,
                                 match_coordinates_sky)
import astropy.units as u
from astropy.stats import mad_std
from astropy.table import Table

import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import NullFormatter

from librgm.plotid import plotid

# could be superseded by astropy.stats.mad_std
def mad_med(data, axis = None):
    return np.median(np.absolute(data - np.median(data, axis)), axis)


def check_matches(files, cols,
                  neighbor,
                  upperlimits=[4, 10.0],
                  printlist=False,
                  debug=False,
                   **keyword_parameter):

    """

    *preforms self-neighbour matching of file and returns diagnostic plots.

    Parameters
    ----------

    files: <type 'str'>
                Name of file

    columns : <type 'ndarray'> or <type 'list'>
                array of column names needed. Must be
                <type 'str'>.

    neighbor: <type 'int'>
                which nth-neighbor match needed.

    Returns
    -------

    matplotlib image

    Examples
    --------

    f1 = "output_DR12_1p44UKIDSSlas_4p0WISE_starL_GMM5QSOs.fits"
    final_array = check_matches(f1,['ra','dec','psfMag_i'],2)
    final_array = check_matches(f1,['ra','dec','psfMag_i'],2, save = '/Desktop/important_plot.png')

    """
    from astropy.table import Table

    figsize=(8,6)

    median_and_mean = [[],[]]

    print('files:', files)
    match_object = files
    columns_object = cols

    # read in the data file
    data = Table.read(files)
    data.info('stats')

    #to_match_RA = fitsio.read(match_object, columns=columns_object[0])
    #to_match_DEC = fitsio.read(match_object, columns=columns_object[1])
    #psfmag=fitsio.read(match_object, columns=columns_object[2])

    #to_match_RA = Table.read(match_object, columns=columns_object[0])
    #to_match_DEC = Table.read(match_object, columns=columns_object[1])
    #psfmag= Table.read(match_object, columns=columns_object[2])

    # help(data)
    # help(to_match_RA)

    print(columns_object[0])
    to_match_RA = data[columns_object[0]]
    to_match_DEC = data[columns_object[1]]
    psfmag = data[columns_object[3]]
    # help(to_match_RA)
    print(to_match_RA.unit)
    print(to_match_RA.shape)
    print(len(to_match_RA), np.min(to_match_RA), np.max(to_match_RA))

    vot = True
    # check units and convert u.deg id needed
    if to_match_RA.unit != 'deg':
        to_match_RA = to_match_RA * u.deg
    if to_match_DEC.unit != 'deg':
        to_match_DEC = to_match_DEC * u.deg

    skycoord_object = SkyCoord(to_match_RA, to_match_DEC,
                                   frame='icrs')

    # matches to self
    idx, d2d, d3d = match_coordinates_sky(skycoord_object, skycoord_object,
                                          nthneighbor=neighbor)
    idx2 = np.asarray([i for i in range(len(idx))])

    #set limits
    separations = np.asarray(d2d)*3600.0

    itest =  (separations < upperlimits[0])
    result = data[itest]
    result_separations = separations[itest]
    print(upperlimits[0])
    print(result_separations)
    if printlist:
        for irow, row in enumerate(result):
            print(irow,
                  row['ra'],
                  row['dec'],
                  row['dist'] * 3600.0,
                  result_separations[irow],
                  row['phot_g_mean_mag'])


    upperlimit = upperlimits[0]
    upperlimit2 = upperlimits[1]
    separations_reduced = separations[(separations<=upperlimit)]
    separations_orig = separations[(separations<=upperlimit2)]
    psfmag_reduced=np.asarray(psfmag)[(separations<=upperlimit)]

    # separations_reduced = separations[(np.asarray(psfmag)<18.0)*(separations<=upperlimit2)]
    # separations_orig = separations[(separations<=upperlimit2)]
    # psfmag_reduced=np.asarray(psfmag)[(np.asarray(psfmag)<18.0)]

    masked_list_ra = np.asarray(skycoord_object.ra)[(idx)]
    masked_list_dec = np.asarray(skycoord_object.dec)[(idx)]
    masked_list_ra_cat = np.asarray(skycoord_object.ra)
    masked_list_dec_cat = np.asarray(skycoord_object.dec)
    # masked = skycoord_object[idx]
    # dra, ddec = skycoord_object.spherical_offsets_to(masked)
    # sky = SkyCoord(masked_list_ra*u.degree, masked_list_dec*u.degree, frame='icrs')
    # dra, ddec = skycoord_object.spherical_offsets_to(sky)
    # dra=float(dra.to(u.arcsec))
    # ddec=float(dra.to(u.arcsec))

    difference_ra = ((((masked_list_ra_cat-masked_list_ra)*np.cos(np.radians(masked_list_dec_cat))))*3600.0)
    difference_dec = (((masked_list_dec_cat-masked_list_dec))*3600.0)

    #final array
    idx_pairs = idx[(separations<=upperlimits[0])]
    idx_pairs_second = idx2[(separations<=upperlimits[0])]

    masked_list_ra_pairs1 = np.asarray(skycoord_object.ra)[(idx_pairs)]
    masked_list_dec_pairs1 = np.asarray(skycoord_object.dec)[(idx_pairs)]

    masked_list_ra_pairs2 = np.asarray(skycoord_object.ra)[(idx_pairs_second)]
    masked_list_dec_pairs2 = np.asarray(skycoord_object.dec)[(idx_pairs_second)]

    median_and_mean = [list(difference_ra),list(difference_dec)]
    median_and_mean = np.asarray(median_and_mean)
    mad_standard = mad_std(median_and_mean)
    mad_median = mad_med(median_and_mean)
    length = len(masked_list_ra)
    length30 = len(separations_reduced)
    med = np.median(separations)
    med_red = np.median(separations_reduced)

    fig = plt.figure(1, figsize=(8,6))
    print('files:', files, len(files))
    print("file: %s" % files)
    plt.suptitle("file: %s"% files, size=10)
    #pylab.title("file: %s"% files,size=14, fontsize='medium')

    ax1=fig.add_subplot(2,2,1)

    print(len(separations_orig))
    print(upperlimit2)
    n, b, patches = ax1.hist(separations_orig,
                             bins=int(upperlimit2/0.5),
                             range=[0.0, upperlimit2],
                             color='green', alpha=0.3)
    bin_min = np.where(n == n.min())
    n1, b1, pathes1 = ax1.hist(separations_reduced,
                               bins=int(upperlimit2/0.5),
                               range=[0.0, upperlimit2],
                               color='blue')
    ax1.set_xlim(0.0, upperlimit2)

    ax1.locator_params(axis='x',nbins=4)

    s0 = 'Matched to self'
    ax1.annotate(s0,(0.28,0.95) , xycoords = 'axes fraction',size=8)
    s04 = '# of Objects = %i'%length
    ax1.annotate(s04,(0.28,0.90) , xycoords = 'axes fraction',size=8)
    s01 = '(All objects) Median = %.2f' % med
    ax1.annotate(s01,(0.28,0.85) , xycoords = 'axes fraction',size=8)
    s03 = '# of objects <= %i arcsecs = %i' % (upperlimit, length30)
    ax1.annotate(s03,(0.28,0.80) , xycoords = 'axes fraction',size=8)
    s02 = '(Objects<=30arcsecs) Median = %.2f' % med_red
    ax1.annotate(s02,(0.28,0.75) , xycoords = 'axes fraction',size=8)

    ax1.set_xlabel('Separation (arcseconds)')
    ax1.set_ylabel('Frequency')

    ax2 = fig.add_subplot(2,2,2)
    markersize = 0.5
    markersize = 1.0
    alpha = 1.0
    ax2.plot(difference_ra, difference_dec,
             'oc',
             markersize=markersize, markeredgewidth=0.0,
             alpha=alpha)
    xrange = [-1.0*upperlimits[1], 1.0*upperlimits[1]]
    yrange = [-1.0*upperlimits[1], 1.0*upperlimits[1]]
    print(xrange + yrange)
    ranges = xrange + yrange
    # ax2.axis('equal')
    ax2.set_aspect('equal')
    ax2.axis(ranges)
    ax2.locator_params(axis='x',nbins=4)
    ax2.set_xlabel('Delta RA (")')
    ax2.set_ylabel('Delta Dec (")')
    # s11 = 'Zoomed-in to 30 arcsecs'
    # ax2.annotate(s11,(0.45,0.95) , xycoords = 'axes fraction',size=8)
    s1 = '# of Objects = %i' % length
    ax2.annotate(s1,(0.45,0.90) , xycoords = 'axes fraction',size=8)
    s7 = 'MAD = %.2f' % mad_median
    ax2.annotate(s7,(0.45,0.85) , xycoords = 'axes fraction',size=8)
    s3 = 'MAD_std = %.2f' % mad_standard
    ax2.annotate(s3,(0.45,0.80) , xycoords = 'axes fraction',size=8)

    ax3 = fig.add_subplot(2,2,3)
    bin_size1=0.25; min_edge1=5;max_edge1=22
    N1 = (max_edge1-min_edge1)/bin_size1; Nplus11 = N1 + 1
    bin_list1 = np.linspace(min_edge1, max_edge1, Nplus11)
    ax3.hist(psfmag_reduced,bins=bin_list1,color='blue')
    xlabel = cols[2]
    ax3.set_xlabel(xlabel)
    ax3.set_ylabel('Frequency')
    ax3.locator_params(axis='x',nbins=4)
    # ax3.plot(to_match_RA,to_match_DEC,'og',markersize=0.5,markeredgewidth=0.0,alpha=0.3)
    # ax3.locator_params(axis='x',nbins=4)
    # ax3.set_xlabel('RA')
    # ax3.set_ylabel('DEC')

    ax4 = fig.add_subplot(2,2,4)
    bin_size=0.25; min_edge=5;max_edge=22
    N = (max_edge-min_edge)/bin_size; Nplus1 = N + 1
    bin_list = np.linspace(min_edge, max_edge, Nplus1)
    ax4.hist(psfmag_reduced,bins=bin_list,color='blue')
    ax4.hist(psfmag,bins=bin_list,color='green',alpha=0.3)
    xlabel = cols[2]
    ax4.set_xlabel(xlabel)
    ax4.set_ylabel('Frequency')
    ax4.locator_params(axis='x',nbins=4)

    fig.tight_layout()
    fig.subplots_adjust(top=0.88)

    plotid()

    if ('save' in keyword_parameter):
        path_to_save = str(keyword_parameter['save'])
        plt.savefig(path_to_save,dpi=150)
    else:
        plt.show()

    return (masked_list_ra_pairs1,masked_list_dec_pairs1,masked_list_ra_pairs2,masked_list_dec_pairs2)


def match_to_dr7_or_dr9(ra_dec_pairs,file_to_match, **keyword_parameter):

    """
    """

    plt.ion()
    catalogue_file = Table.read(file_to_match)
    cat_RA = catalogue_file['RA_dr7qso']
    cat_DEC = catalogue_file['DEC_dr7qso']
    object_table = Table([ra_dec_pairs[0],ra_dec_pairs[1],ra_dec_pairs[2],ra_dec_pairs[3]]\
        ,names=('obj1_RA, obj1_DEC, obj2_RA, obj2_DEC'))
    object_RA = object_table['obj1_RA']
    object_DEC = object_table['obj1_DEC']

    skycoord_cat = SkyCoord(cat_RA*u.degree,cat_DEC*u.degree, frame='icrs')
    skycoord_object = SkyCoord(object_RA*u.degree,object_DEC*u.degree, frame='icrs')
    idx, d2d, d3d = match_coordinates_sky(skycoord_cat, skycoord_object)
    separations = np.asarray(d2d)*3600.0
    upperlimit = 30.0
    separations_reduced = separations[(separations<=upperlimit)]

    masked_list_ra = np.asarray(skycoord_object.ra)[(idx)]
    masked_list_dec = np.asarray(skycoord_object.dec)[(idx)]

    masked_list_ra_cat = np.asarray(skycoord_cat.ra)
    masked_list_dec_cat = np.asarray(skycoord_cat.dec)

    difference_ra = ((masked_list_ra_cat-masked_list_ra)*np.cos(np.radians(masked_list_dec_cat)))*3600.0
    difference_dec = (masked_list_dec_cat-masked_list_dec)*3600.0

    fig = plt.figure(1, figsize=(8,6))
    ax1=fig.add_subplot(1,2,1)
    ndata = len(separations_reduced)
    ax1.hist(separations_reduced,bins=upperlimit/0.5, label=str(ndata))
    ax1.set_title("MATCH TO DR7")
    ax1.set_xlabel('Separation (arcseconds)')
    ax1.set_ylabel('Frequency')
    ax1.legend(loc='upper right')


    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(difference_ra,difference_dec,'oc',markersize=5.0,alpha=0.3)
    ax2.locator_params(axis='x',nbins=4)
    ax2.set_title("MATCHED PAIRS")
    ax2.set_xlabel('DELTA RA')
    ax2.set_ylabel('DELTA DEC')
    plt.tight_layout(pad=0.4, w_pad=0.5)

    if ('save' in keyword_parameter):
        path_to_save = str(keyword_parameter['save'])
        plt.savefig(path_to_save,dpi=150)
    else:
        plt.show()

if __name__ == "__main__":

    import time
    import argparse
    import ConfigParser

    import matplotlib as mpl
    print('matplotlib.get_backend():', mpl.get_backend())

    t0 = time.time()

    # input files
    f1 = "output_DR12_1p44UKIDSSlas_4p0WISE_starL_GMM5QSOs.fits"
    f2 = "dr7qso_new.fits"
    f3 = "dr9qso.fits"

    # read input files from config file
    config = ConfigParser.ConfigParser()
    print('__file__:', __file__)
    configfile = os.path.splitext(__file__)[0] + '.cfg'
    print('Read configfile:', configfile)
    config.read(configfile)

    f1 = config.get('DEFAULT', 'f1')
    f2 = config.get('DEFAULT', 'f2')
    f3 = config.get('DEFAULT', 'f3')

    description = ''' '''
    epilog = " "

    # use formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # so that --help lists the defaults
    parser =  argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    print('Processing:', f1)
    neighbour = 2
    final_array=check_matches(f1, ['ra','dec','psfMag_i'],
                               neighbour, save='./check_matching.png')
    # y=match_to_dr7_or_dr9(x, f2, save = '/Users/Chris_Desira/desktop/Machine_learning/important/images/dr7_match.png')


    print('Elapsed time(secs): ',time.time() - t0)
