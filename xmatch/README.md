

Various high level positional cross matching functions based on astropy
that are under development.

e.g. checkplots is currently be rationalised. Please be patient

They take either a ra, dec lists of values in units of degrees or astropy tables
with aribitrary units. For astropy tables the column names are specified
as arguments.

See:

* http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html
* http://docs.astropy.org/en/stable/coordinates/matchsep.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html

Astropy has two ‘methods’ or ‘functions’: One is a function and the other
is a SkyCoord method which can lead to some confusion. i.e. it confused me.

    
## match_coordinates_sky and match_to_catalog_sky

Finds the nearest or nth neighbour on-sky matches of a coordinate or
coordinates in a set of catalog coordinates.

###  match_coordinates_sky
    
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html

match_coordinates_sky is a function

match_to_catalog_sky is a Skycoord method

Both return identical results


```   
     match_coordinates_sky(
         matchcoord, catalogcoord, nthneighbor=1,
         storekdtree=u'_kdtree_sky')

     returns idx, sep2d, sep3d
```

e.g.

```

idx, d2d, d3d = match_coordinates_sky(skycoord1, skycoord2)  

or

idx, d2d, d3d = skycoord1.match_to_catalog_sky(skycoord2)

```

    
### (2) SkyCoord.match_to_catalog_sky

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


## Multiple matching within a radius

called Searching Around Coordinates in astropy

```
idx1, idx2, d2d, d3d = \
    SkyCoord1.search_around_sky(SkyCoord2, 10.0*u.arcsec)
```

The key difference for these methods is that there can be multiple (or no)
matches in catalog around any locations in c. Hence, indices into both
skycoord1 and skycoord2 are returned instead of just indices into catalog.
These can then be indexed back into the two SkyCoord objects, or, for that
matter, any array with the same order:



ra, dec list could maybe be a zipped i.e. radec = zip(ra, dec)

also, could work out the input data form internally; table versus list

The broad idea is makes the functions as easy to use as TOPCAT and STILTS.


### Some good practice suggestions

It is good practice to write the input filename into the table metadata.

table.meta['filename'] = filename

You can then check it if it is present later with:
if 'filename' in table.meta:
    print('filename:', filename)
