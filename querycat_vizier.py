"""
ported from

https://michaelmommert.wordpress.com/2017/02/13/accessing-the-gaia-and-pan-starrs-catalogs-using-python/


see also querycat_gaia

astroquery.readthedocs.io/en/latest/vizier/vizier.html

CDS Vizier:
PS1: II/349/ps1
SDSSDR9: V/139/sdss9
GaiaDR1: I/337/gaia
ALLWISE: II/328/allwise

could store these in a dict


"""

import sys
import time

from astropy.table import Table, vstack

import astropy.units as u
from astropy.coordinates import SkyCoord, Angle

from astroquery.vizier import Vizier

def querycat_vizier(ralist=None,
                    declist=None,
                    catalog="II/349/ps1",
                    radius=10.0,
                    width=20.0, height=20.0,
                    maxsources=10000,
                    catname='PS1',
                    tap=False,
                    verbose=False, debug=False):
    """

    radius could be a list to support different search radius or window
    for each source.

    Query PS1 catalogue at CDS Vizier using astroquery.vizier

    parameters: ra_deg, dec_deg, rad_deg: RA, Dec, field
                                          radius in degrees
                maxmag: upper limit G magnitude (optional)
                maxsources: maximum number of sources

    returns: astropy.table object

    """

    vizier_catalogs = {"PS1": 'II/349/ps1',
                       "SDSSDR9": 'V/139/sdss9',
                       "GaiaDR1": 'I/337/gaia',
                       "ALLWISE": 'II/328/allwise'}

    if debug:
        help(Vizier)

    adql = ""

    if verbose or debug:
        print('radius:', radius)
    radius = u.Quantity(radius/3600.0, u.degree)
    if verbose or debug:
        print('radius:', radius)

    result_nrows = 0
    for isource, (ra, dec) in enumerate(zip(ralist, declist)):

        coord = SkyCoord(ra=ra, dec=dec,
                         unit=(u.deg, u.deg),
                         frame='icrs')

        print(isource, coord)
        # query = Vizier(catalog=catalog))

        # the [0] is since Vizier can return results from more than 1 table
        try:
            result = Vizier.query_region(coord,
                                         radius=radius,
                                         catalog=catalog)
        except:
             pass

        print('result:', isource, len(result))
        # print(result)

        # need to allow for fact that searchs can reture 0 rows
        if isource == 0:
            result_all = []

        if len(result) != 0:
            result = result[0]
            print('result:', isource, len(result))
            result_nrows = result_nrows + len(result)
            if len(result_all) == 0:
                result_all = result
            if len(result_all) > 0:
                print(len(result_all), len(result))
                result_all = vstack([result_all, result])

    print('Total number of rows returned:', len(result_all))

    return result_all

if __name__=='__main__':

    # print(Vizier.find_catalogs('PS1'))

    # help(Vizier)

    ralist = [180.0]
    declist = [0.0]

    radius = 30.0
    print(ps1_query(ralist=ralist,
                    declist=declist,
                    radius=radius,
                    debug=False))


    catalog = 'V/139/sdss9'
    radius = 30.0
    print(ps1_query(ralist=ralist,
                    declist=declist,
                    radius=radius,
                    catalog=catalog))
