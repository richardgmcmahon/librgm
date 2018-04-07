def fix_votable_object(table, verbose=False):
    """
    convert the columns with dtype = object which is not
    supported by FITs to bool
    """

    for (icol, column) in enumerate(table.columns):
        if verbose:
            print(icol, table.columns[icol].name,
                table.columns[icol].format,
                table.columns[icol].dtype)

        if table.columns[icol].dtype == 'object':
            colname = table.columns[icol].name
            NewColumn = Table.Column(table[colname].data, dtype='bool')
            table.replace_column(colname, NewColumn)

    return table
