def fix_votable_object(table):
    """

    """
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

    return table
