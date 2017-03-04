def table_info_stats(table=None, short=False, stats=True, debug=False):
  """print some info about astropy table

  CAVEAT: astropy does some fancy masking when there is missing/bad data

  """

  ncolumns=len(table.columns)

  print('Number of rows: ', len(table))
  print('Number of columns: ', ncolumns)
  print('meta: ', table.meta)
  print('dtype: ', table.dtype)
  print('colnames: ', table.colnames)

  columns = table.columns
  if debug: print(table)
  if debug: print(len(table.columns[0]))
  if debug: print(len(table.field(0)))

  #help(table.columns)
  #help(table.field)

  if stats or not short:
    for i in xrange(ncolumns):
      j=0

      # process the columns that are 1D vectors
      if len(table.columns[i].shape) == 1:
        try:
          print(i, j, table.columns[i].name, table.columns[i].format,\
           table.columns[i].shape, len(table.columns[i].shape), \
           len(table.columns[i]), \
          ': ',np.min(table.columns[i]), ' : ',np.max(table.columns[i]))

        except:
           print(i, j, table.columns[i].name, 'problem with column')
           pass


      # process the columns that are 2D vectors (i,j)
      if len(table.columns[i].shape) == 2:
        for j in xrange(table.columns[i].shape[1]):
          print(i,j, columns[i].name, columns[i].format, \
           columns[i].dim, table.columns[i].shape, \
           len(table.field(i).shape), \
           len(table.field(i)), \
           ': ',np.min(table.field(i)[j]),' : ',np.max(table.columns[i][j]))
