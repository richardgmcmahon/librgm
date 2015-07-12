def table_index_column(table=None, colname=None, casesensitive=False):
  """

  astropy table function; could be modified to also support pyfits and
  Erin Sheldons fitsio
 
  includes caseinsensive option

  see also astropy.Table.index_column
  
  return icol = -1 if no column exists


  """

  if casesensitive:
    icol=table.colnames.index('colname')

  if not casesensitive:
    icol=map(str.lower,table.colnames).index('colname')

  if icol < 0: print('Column {0} does not exist'.format(colname))

  return icol
