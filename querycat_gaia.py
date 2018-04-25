"""

get remote Gaia data using astropy.astroquery

astroquery.gaia uses the ESA archive; we could add option to use
CDS Vizier via TAP or Vizier cone search

sychronous and asychronous queries are supported
with current (2018, April) timeouts of 1min and 30min

Launched query:
'SELECT DISTANCE(POINT('ICRS',ra,dec),
POINT('ICRS',304.82563658,11.4523159813)) AS dist, *
FROM gaiadr1.gaia_source
WHERE
CONTAINS(POINT('ICRS',ra,dec), BOX('ICRS',304.82563658,11.4523159813, 0.00555555555556, 0.00555555555556)) = 1
ORDER BY dist ASC'

"""
def querycat_gaia(ralist=None, declist=None, cone_search=False,
                width=10.0, height=10.0, radius=5.0,
                test=False, debug=False):
    """


    """

    import time

    from astropy.table import Table, vstack

    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astroquery.gaia import Gaia

    if debug:
        help(Gaia)

    width = u.Quantity(width/3600.0, u.degree)
    height = u.Quantity(height/3600.0, u.degree)
    radius = u.Quantity(radius/3600.0, u.degree)


    if test is True:
        ralist = [180.0]
        declist = [0.0]

        width = u.Quantity(30.0, u.arcsec)
        height = u.Quantity(30.0, u.arcsec)
        radius = u.Quantity(15.0, u.arcsec)


    result_nrows = 0
    for isource, (ra, dec) in enumerate(zip(ralist, declist)):

        coord = SkyCoord(ra=ra, dec=dec,
                         unit=(u.degree, u.degree),
                         frame='icrs')

        t0 = time.time()
        if not cone_search:
            result = Gaia.query_object_async(coordinate=coord,
                                             width=width, height=height)
            # help(result)
            if debug:
                result.pprint()
                result.info('stats')

        if cone_search:
            job = Gaia.cone_search_async(coord, radius)
            # help(job)
            result = job.get_results()

        print('Number of rows:', len(result))
        print('Elapsed time(secs):',time.time() - t0)

        if debug:
           help(result)
           result.pprint()
           result.info('stats')


        result_nrows = result_nrows + len(result)
        if isource == 0:
            result_all = result
        if isource > 0:
           result_all = vstack([result_all, result])

#def fix_vot_object():
    table = result_all
    print('icol, format, dtype')
    # help(table)
    # help(table.columns)
    for (icol, column) in enumerate(table.columns):
        print(icol, table.columns[icol].name,
              table.columns[icol].format,
              table.columns[icol].dtype)
        # convert the columns for dtype = object which is not
        # supported by FITs to bool
        if table.columns[icol].dtype == 'object':
            colname = table.columns[icol].name
            NewColumn = Table.Column(table[colname].data, dtype='bool')
            table.replace_column(colname, NewColumn)
    print()


    result_all = table

    print('Number of Gaia sources returned:', result_nrows, len(result_all))

    return result_all
