

Various positional cross matching functions that are under development.

They take either a ra, dec lists in units of degrees or astropy tables
with aribitrary units. For astropy tables the column names are specified
as arguments.

ra, dec list could maybe be a zipped i.e. radec = zip(ra, dec)

also, could work out the input data form internally; table versus list

The broad idea is makes the functions as easy to use as TOPCAT and STILTS.


It is good practice to write the input filename into the table metadata.

table.meta['filename'] = filename

You can then check it if it is present later with:
if 'filename' in table.meta:
    print('filename:', filename)
