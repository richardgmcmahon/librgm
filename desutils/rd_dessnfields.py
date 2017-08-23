def rd_dessnfields(infile=None,
                   fields = ['E1', 'E2', 'S1', 'S2',
                             'C1', 'C2', 'C3', 'X1', 'X2', 'X3'],
                   debug=False):
    """
    Read the DES SN field centres

    """
    import ConfigParser

    import numpy as np

    from astropy.coordinates import SkyCoord
    from astropy import units as u

    nfields = len(fields)

    infile = 'des_snfields.cfg'
    print('Read file:', infile)

    config = ConfigParser.ConfigParser()
    config.read(infile)
    print('file sections:', config.sections())

    ra = np.empty(nfields, dtype=np.float64)
    dec = np.empty(nfields, dtype=np.float64)
    print(len(ra), ra)

    ifield = -1
    for field in fields:
        ifield = ifield + 1
        fieldname = 'RADEC_' + field
        radec_field = config.get('DEFAULT', fieldname)

        radec = SkyCoord(radec_field,  unit=(u.hour, u.deg))
        print('fieldname; RA, Dec:', ifield, fieldname, radec_field,
              radec.ra.deg, radec.dec.deg)

        ra[ifield] = radec.ra.deg
        dec[ifield] = radec.dec.deg

    return ra, dec
