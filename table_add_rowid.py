def table_add_rowid(nrows=1, colname='rowid'):
    """

    add an an integer rowid column starting at 1 to an astropy table

    to save bit I use int32 for tables with < 2^31 = 2147483648
    = 2.15 billion rows

    int16 would work for tables with less than 32k rows

    int64 works for upto 9 x 10^18; 9 billion billion

    """
    import numpy as np
    from astropy.table import Table

    debug = True
    if debug:
        print('nrows:', nrows)

    if nrows < 2e9:
        rowid_dtype = np.int32
    if nrows >= 2e9:
        rowid_dtype = np.int64

    rowid = np.arange(1, nrows + 1, step=1, dtype=rowid_dtype)
    if debug:
        print(rowid[0], rowid[-1])

    table = Table()
    table[colname] = rowid

    if debug:
        table.info()
        table.info('stats')

    return table
