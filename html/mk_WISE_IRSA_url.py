def mk_WISE_IRSA_url(RA, Dec, size=None, output_size=None, zoom_factor=1.0):
    """

    Default:


http://irsa.ipac.caltech.edu/applications/wise/

#id=Hydra_wise_wise_1&RequestClass=ServerRequest&DoSearch=true&intersect=CENTER&subsize=0.16666666800000002&mcenter=mcen&schema=allwise-multiband&dpLevel=3a&band=1,2,3,4
&UserTargetWorldPt=46.53;-0.251;EQ_J2000
&SimpleTargetPanel.field.resolvedBy=nedthensimbad&preliminary_data=no&coaddId=&projectId=wise&searchName=wise_1&shortDesc=Position&isBookmarkAble=true&isDrillDownRoot=true&isSearchResult=true


    """

    url_base = 'http://irsa.ipac.caltech.edu/applications/wise/'

    url_head = '#id=Hydra_wise_wise_1&RequestClass=ServerRequest&DoSearch=true&intersect=CENTER&subsize=0.16666666800000002&mcenter=mcen&schema=allwise-multiband&dpLevel=3a&band=1,2,3,4'

    url_tail = '&SimpleTargetPanel.field.resolvedBy=nedthensimbad&preliminary_data=no&coaddId=&projectId=wise&searchName=wise_1&shortDesc=Position&isBookmarkAble=true&isDrillDownRoot=true&isSearchResult=true'

    url = "<A HREF = " + url_base + url_head + \
        "&UserTargetWorldPt=" + \
        str("%.5f" % RA) + ";" + str("%.5f" % Dec) + ';EQ_J2000' + \
       url_tail + \
       "> IRSA_WISE </A>"

    return url
