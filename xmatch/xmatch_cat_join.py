from __future__ import print_function, unicode_literals

def xmatch_cat_join(table1=None, table2=None,
                    idxmatch=None,
                    jointype='left',
                    dr=None, radius_arcsec=2.0):
    """

    looks like just a nearest neighbour match is supported


    """
    from astropy.table import Table, hstack

    # rows in table2 that match with table1
    table2_xmatch_table1 = table2[idxmatch]

    # paste table2 columns onto the table1 rows
    print(len(table2_xmatch_table1))
    result = hstack([table1, table2_xmatch_table1])
    print('Number of rows in hstack table:', len(result))

    # create table with sources that match with in radius of 10"
    itest = dr < radius_arcsec
    print('Number of matched sources within ', radius_arcsec, 'arcsec',
          len(table1[itest]))
    result = result[itest]

    return result
