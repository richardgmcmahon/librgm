

Various positional cross matching functions that are under development.

e.g. checkplots is currentlyt be rationalised. be patient

They take either a ra, dec lists of values in units of degrees or astropy tables
with aribitrary units. For astropy tables the column names are specified
as arguments.

See:

* http://docs.astropy.org/en/stable/coordinates/matchsep.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html

Astropy has two ‘methods’ or ‘functions’: One is  a function and a method
which can lead to some confusion. i.e. it confused me.

    
## match_coordinates_sky and match_to_catalog_sky
    
###  (1) astropy.coordinates.match_coordinates_sky
    
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html#astropy.coordinates.match_coordinates_sky
```   
     match_coordinates_sky(
         matchcoord, catalogcoord, nthneighbor=1,
         storekdtree=u'_kdtree_sky')

     returns idx, sep2d, sep3d
```    
 Finds the nearest or nth neighbour on-sky matches of a coordinate or
 coordinates in a set of catalog coordinates.
    
match_coordinates_sky is a python function
    
### (2) astropy.coordinates.match_coordinates_sky

* http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord.match_to_catalog_sky
    #
    #
    #
    #  returns idx, sep2d, sep3d
    #
    #
    # Finds the nearest on-sky matches of this coordinate in a set of
    # catalog coordinates.
    #
    # For more on how to use this (and related) functionality, see the
    # examples in Separations, Catalog Matching, and Related Functionality.
    #
    #  match_to_catalog_sky is a python method



ra, dec list could maybe be a zipped i.e. radec = zip(ra, dec)

also, could work out the input data form internally; table versus list

The broad idea is makes the functions as easy to use as TOPCAT and STILTS.


It is good practice to write the input filename into the table metadata.

table.meta['filename'] = filename

You can then check it if it is present later with:
if 'filename' in table.meta:
    print('filename:', filename)
