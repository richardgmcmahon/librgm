from __future__ import division, print_function

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u


def mk_radecname(ra, dec, precision=0, prefix='',
                 shortform=False):
    """ make a radec name from ra, dec e.g. HHMMSSsDDMMSS


    """

    sep = ''

    radec = SkyCoord(ra=ra * u.degree, dec=dec * u.degree)
    if not shortform:
        radecname = radec.to_string('hmsdms', decimal=False,
                                    sep=sep,
                                    precision=precision)

    if shortform:
        radec_string = radec.to_string('hmsdms', decimal=False,
                                       sep=sep, precision=0)
        radecname = radec_string[0:4] + radec_string[7:12]

    radecname = np.core.defchararray.replace(radecname, ' ', '')

    if prefix != '':
        # radecname = prefix + radecname does not work
        radecname = np.core.defchararray.add(prefix, radecname)

    return str(radecname)


def mk_jname(ra, dec, sep='', prefix='J', shortform=False):
    """

    http://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html#astropy.coordinates.Angle.to_string

    """

    radec = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='icrs')

    if not shortform:
        jname = radec.to_string('hmsdms', decimal=False,
                                sep=sep, precision=2)
        jname = jname.replace(' ', sep)
        jname = prefix + jname
        jname = jname[:-1]

    if shortform:
        radec_string = radec.to_string('hmsdms', decimal=False,
                                       sep=sep, precision=0)
        jname = prefix + radec_string[0:4] + radec_string[7:12]

    return jname


if __name__=='__main__':

    import time

    import numpy as np

    t0 = time.time()

    n = 10000
    ra = np.zeros(n)
    dec = np.zeros(n)

    t0 = time.time()
    radecnames = mk_radecname(ra, dec, precision=0, prefix='')
    print('radecnames[0]:', radecnames[0])
    print('Elapsed time:', time.time() - t0)

    t0 = time.time()
    radecnames = mk_radecname(ra, dec, precision=0, prefix='J')
    print('radecnames[0]:', radecnames[0])
    print('Elapsed time:', time.time() - t0)

    t0 = time.time()
    for isource, source in enumerate(ra):
        radecnames = mk_radecname(ra[isource], dec[isource],
                                  precision=0, prefix='')
    print('Run loop:', n)
    print('Elapsed time:', time.time() - t0)


    t0 = time.time()
    for isource, source in enumerate(ra):
        radecnames = mk_radecname(ra[isource], dec[isource],
                                  precision=0, prefix='J')
    print('Run loop:', n)
    print('Elapsed time:', time.time() - t0)

    ra = 180.0
    dec = -0.1


    radecname = mk_radecname(ra, dec, precision=1, prefix='')
    print('radecname:', radecname)


    ra = 180.0
    dec = 0.2

    radecname = mk_radecname(ra, dec, precision=0, prefix='')
    print('radecname:', radecname)


    radecname = mk_radecname(ra, dec, precision=1, prefix='')
    print('radecname:', radecname)
