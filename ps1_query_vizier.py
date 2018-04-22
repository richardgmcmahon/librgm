"""
ported from

https://michaelmommert.wordpress.com/2017/02/13/accessing-the-gaia-and-pan-starrs-catalogs-using-python/

"""

from astroquery.vizier import Vizier
import astropy.units as u
import astropy.coordinates as coord

def ps1_query_vizier(ra_deg, dec_deg, rad_deg, maxmag=None,
               maxsources=10000):
    """

    Query Gaia DR1 @ VizieR using astroquery.vizier
    parameters: ra_deg, dec_deg, rad_deg: RA, Dec, field
                                          radius in degrees
                maxmag: upper limit G magnitude (optional)
                maxsources: maximum number of sources
    returns: astropy.table object

    """

    vquery = Vizier(columns=['Source', 'RA_ICRS', 'DE_ICRS',
                             'phot_g_mean_mag'],
                    column_filters={"phot_g_mean_mag":
                                    ("<%f" % maxmag)},
                    row_limit = maxsources)

    field = coord.SkyCoord(ra=ra_deg, dec=dec_deg,
                           unit=(u.deg, u.deg),
                           frame='icrs')

    catalog = "II/349/ps1"
    return vquery.query_region(field,
                               width=("%fd" % rad_deg),
                               catalog=catalog)[0]


# Example query
# print(gaia_query(12.345, 67.89, 0.1))
