
def mk_radec_vot(table=None, label='source',
                 colnames_radec=('ra', 'dec')):
    """
    create and write a thin votable format file for upload to CDS and ESA
    with the addition of a source ID column.

    """

    from astropy.io.votable import from_table, writeto

    nrows = len(table)
    print('nrows:', nrows)
    colname_rowid = label + '_id'
    rowid = table_rowid(nrows=nrows, colname=colname_rowid)
    rowid.info()
    table_out = Table()
    table_out[colname_rowid] = rowid[colname_rowid]
    table_out['ra_' + label] = table[colnames_radec[0]]
    table_out['dec_' + label] = table[colnames_radec[1]]
    table_out.info()
    table_out.info('stats')
    print()

    print('Convert table to votable')
    votable = from_table(table_out)
    print('Elapsed time(secs):', time.time() - t0)
    print()

    outfile = label + "_radec.vot"

    print('Write VOT format file with io.votable.writeto:', outfile)
    writeto(votable, outfile,
            tabledata_format='binary')
    print()

    print('Write VOT format file with table.write:', outfile)
    table_out.write(outfile,
                    table_id=label,
                    format='votable',
                    tabledata_format='binary',
                    overwrite=True)
    print()

    infile = outfile
    print('Read VOT format file with table.write:', infile)
    test = Table.read(infile)
    print()
    test.info('stats')

    return
