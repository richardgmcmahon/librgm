def table_index_column(table=None, colname=None, casesensitive=False, debug=False):
  """

  see also astropy.Table.index_column

  http://astropy.readthedocs.org/en/latest/api/astropy.table.Table.html#astropy.table.Table.index_column
  
  could deprecate and use the astropy version and make the 
  case sensitive support via either changing the colnames in main code
  or via trying both cases sequentially.

  astropy table function; could be modified to also support pyfits and
  Erin Sheldons fitsio
 
  includes non case sensitive option

  return icol = -1 if no column exists


  """

  if debug:
    print(table.colnames)
    print
    print('column name: ', colname)

  if casesensitive:
    icol=table.colnames.index(colname)

  if not casesensitive:
    icol=map(str.lower,table.colnames).index(colname)

  if debug:
    print('column number: ', icol)

  if icol < 0: print('Column {0} does not exist'.format(colname))

  return icol
