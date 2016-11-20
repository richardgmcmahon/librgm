"""
This started from a copy of FHTML.py from Fernanda Ostrovski in June 2016
It is based on a version of HTML from Sophie Reed. The current version
of HTML.py from Sophie has a creation date of 20150116


We might want to explore the use of:

  https://pypi.python.org/pypi/html

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np


def table(term_list, header_list, links=(False, 0, [])):
    """
    create a html table
    """

    print("running function:", __name__)
    print('Number of rows:', len(term_list))
    print('Number of column fields:', len(header_list))

    lines = ""

    # rgm added anchor support <a name="anchor"></a>
    # where anchor is the row number ID as a string
    # a url of the form base_url#ID then takes you to the row you want.

    irow = -1
    for term in term_list:

        irow = irow + 1
        n = 0
        p = term_list.index(term)

        while n < len(term):

            if (links[0] is True) and (links[1] == n):
                file = str(links[2][p]) + ".html"
                st = link(file, str(term[n]))

            else:
                st = str(term[n])

            if n == 0:
                line = "<TR><TD>" + '<A href=#' + str(p + 1) + '>' \
                       + str(p + 1) + '</A>' + \
                       '<a name="' + str(p + 1) + '"></a>' + \
                         "</TD><TD>" + st + "</TD>"
            elif n == len(term) - 1:
                line += "<TD>" + st + "</TD></TR>\n"
            else:
                line += "<TD>" + st + "</TD>"

            n += 1

        lines += line

    heads = ""
    n = 0
    while n < len(header_list):
        head = header_list[n]
        if n == 0:
            heads += '<script src="sorttable.js"></script>\n' \
                + '<TABLE BORDER=1 ' \
                + 'class="sortable tableWithFloatingHeader">\n' \
                + '<THEAD><TR><TH><B>ID </B></TH><TH><B>' \
                + head + "</B></TH>"
        elif n == len(header_list) - 1:
            heads += "<TH><B>" + head + "</B></TH></THEAD></TR>\n<TBODY>\n"
        else:
            heads += "<TH><B>" + head + "</B></TH>"

        n += 1

    lines = heads + lines + "\n</TBODY>\n</TABLE>"

    if len(term_list) == 0:
        print("No values to turn into table")
        return
    else:
        return lines


def image(im_file):
    """
    create image link
    """

    im_line = "<img src=" + im_file + ">"
    return im_line


def link(link_add, link_text):
    """
    create link
    """
    link_line = "<a href=" + link_add + ">" + link_text + "</a>"
    return link_line


def cutout_page(link_path, link_add, cutout_files, info, RA_main):
    """
   create cutout page
    """
    f = open(link_path + link_add, "w")
    lines = ""

    for (i, j) in info:
        if i == RA_main:
            l = info.index((i, j))
        line = str(i) + ": " + str(j) + "<BR>"
        lines += line

    lines += wise_url(info[l][1], info[l + 1][1]) + "<BR>"
    lines += ned_url(info[l][1], info[l + 1][1]) + "<BR>"
    lines += sdss_url(info[l][1], info[l + 1][1]) + "<BR>"
    lines += dr9_url(info[l][1], info[l + 1][1]) + "<BR>"
    lines += dr12_url(info[l][1], info[l + 1][1]) + "<BR>"
    for cutout_file in cutout_files:
        print(cutout_file)
        lines += "<BR>" + "<center>" + str(cutout_file) + "<BR>" \
            + image(cutout_file) + "</center>" + "<BR><BR>"

    f.write(lines)
    f.close()


def wise_url(RA, DEC):
    """
    create WISE IRSA link
    """
    if isinstance(RA, np.float):
        RA = "%.5f" % RA
        DEC = "%.5f" % DEC

    line = '<a href="http://irsa.ipac.caltech.edu/applications/wise/' \
        + '#id=Hydra_wise_wise_1&RequestClass=ServerRequest&' \
        + 'DoSearch=true&intersect=CENTER&subsize=0.1&' \
        + 'mcenter=mcen&schema=allsky-4band&dpLevel=3a&band=1,2,3,4&' \
        + 'UserTargetWorldPt=' \
        + str(RA) + ';' + str(DEC) \
        + ';EQ_J2000&' \
        + 'SimpleTargetPanel.field.resolvedBy=nedthensimbad&' \
        + 'preliminary_data=no&coaddId=&projectId=wise&' \
        + 'searchName=wise_1&shortDesc=Position&isBookmarkAble=true&' \
        + 'isDrillDownRoot=true&isSearchResult=true">' \
        + 'The coordinates in WISE</A>'

    return line


def ned_url(RA, DEC):
    """
    create NED link from string or floating point RA, Dec

    """
    if isinstance(RA, np.float):
        RA = "%.5f" % RA
        DEC = "%.5f" % DEC

    # line = '<a href="http://ned.ipac.caltech.edu/cgi-bin/objsearch?' \
    #    + 'search_type=Near+Position+Search' \
    #    + '&in_csys=Equatorial&in_equinox=J2000.0&lon=' \
    #    + RA + 'd&lat=' + DEC + 'd&radius=2.0">NED Link</a>'

    # change RA, DEC to str(RA), str(DEC)
    line = '<a href="http://ned.ipac.caltech.edu/cgi-bin/objsearch?' \
        + 'search_type=Near+Position+Search' \
        + '&in_csys=Equatorial&in_equinox=J2000.0&lon=' \
        + str(RA) + 'd&lat=' + str(DEC) + 'd&radius=2.0">NED Link</a>'

    return line


def sdss_url(RA, DEC):
    """
    create SDSS DR7 cas/skyserver explore link
    """
    line = '<a href="http://cas.sdss.org/dr7/en/tools/explore/obj.asp?' \
        + 'ra=' + RA + '&dec=' + DEC + '">SDSS Skyserver Link</a>'

    return line


def dr9_url(RA, DEC):
    """
    create SDSS skyserver DR9 navigate link
    """
    line = '<A HREF = "' \
        + 'http://skyserver.sdss3.org/dr9/en/tools/chart/navi.asp?' \
        + 'ra=' + RA + "&dec=" + DEC + '">SDSS DR9 Navigate Tool Link</A>'

    return line


def dr12_url(RA, DEC):
    """
    create SDSS skyserver DR12 navigate link
    """
    line = '<A HREF = ' \
        + '"http://skyserver.sdss3.org/dr12/en/tools/chart/navi.aspx?' \
        + 'ra=' + RA + '&dec=' + DEC + '">SDSS DR12 Navigate Tool Link</A>'

    return line


if __name__ == "__main__":

    help(__name__)
