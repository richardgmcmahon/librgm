def mk_ned_url(RA, DEC, radius=1.0, debug=False, verbose=False):
    """

    """
    link = "<A HREF=http://ned.ipac.caltech.edu/cgi-bin/objsearch?" \
           + "search_type=Near+Position+Search&in_csys=Equatorial&" \
           + "in_equinox=J2000.0&lon=" + str("%.5f" % RA) \
           + "d&lat=" + str("%.5f" % DEC) + "d&radius=" \
           + str(radius) + ">NED Link</A>"

    if debug or verbose:
        print(link)

    return link
