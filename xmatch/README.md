

Various high level positional cross matching functions based on astropy
that are under development.

The goal is to be as easy to use as TOPCAT and STILTS and give comparable results:

* STILTS: http://www.star.bris.ac.uk/~mbt/stilts/sun256/match.html
* TOPCAT: http://www.star.bris.ac.uk/~mbt/topcat/sun253/sun253.html
  * http://www.star.bris.ac.uk/~mbt/topcat/sun253/sun253.html#matchCriteria

Note: checkplot# is currently be rationalised. Please be patient

The fucntions take either a ra, dec lists of values in units of degrees
or as astropy table columns with aribitrary units. For astropy tables the
column names are specified as arguments.

See:

* [Separations, Catalog Matching, and Related Functionality](http://docs.astropy.org/en/stable/coordinates/matchsep.html)
* http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html
* http://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html

    
## Nearest or nth nearest neighbour match: match_coordinates_sky; match_to_catalog_sky


Finds the nearest or nth neaarest neighbour on-sky matches for a coordinate or
list of coordinates in catalog or table.

* match_coordinates_sky is a function
* match_to_catalog_sky is a Skycoord method.

Both return identical results.

###  match_coordinates_sky [source](http://docs.astropy.org/en/stable/_modules/astropy/coordinates/matching.html#match_coordinates_sky)
    
* http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html


```   
    match_coordinates_sky(matchcoord,
                          catalogcoord,
                          nthneighbor=1,
                          storekdtree=u'_kdtree_sky')

     .....

     return idx, sep2d, sep3d
```

e.g.

```
    idx2, d2d, d3d = match_coordinates_sky(skycoord1, skycoord2)  

```

idx2 is index to object in skycoord2. idx2 has the same number of elements
as skycoord1. i.e. len(idx2) = len(skycoord2)
    
### match_to_catalog_sky (SkyCoord method) [source](http://docs.astropy.org/en/stable/_modules/astropy/coordinates/sky_coordinate.html#SkyCoord.match_to_catalog_sky)


* http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord.match_to_catalog_sky


For search_around_sky which returns 0 to n matches within a
search radius the function and method have the same name.

It would be convenient is maybe if the match_coordinates_sky function
was renamed as match_to_catalog_sky. It would be worth checking that
it does not already exist as a function name.

match_to_catalog_sky(catalogcoord, nthneighbor=1)


```
idx, d2d, d3d = skycoord1.match_to_catalog_sky(skycoord2)
```


## Multiple matching within a radius: search_around_sky

called Searching Around Coordinates in astropy

SkyCoord.search_around_sky like SkyCoord match_to_catalog_sky is a
SkyCoord method.

* method: http://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord.search_around_sky

```

search_around_sky(searcharoundcoords, seplimit)

idx1, idx2, d2d, d3d = \
    SkyCoord1.search_around_sky(SkyCoord2, 10.0*u.arcsec)
```


* function: http://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html

```
idx1, idx2, d2d, d3d = \
    astropy.coordinates.search_around_sky(SkyCoords1, SkyCoords2,
                                          seplimit,
                                          storekdtree='kdtree_sky'

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
