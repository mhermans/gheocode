
# Introduction

fed up with the detour using pyspatialite, libgeos.so 

reinstalling pyspatialite results in cryptic download errors, which should be resolvable by a http://danielsokolowski.blogspot.be/2013/02/geodjango-spatialite-sqlite3-setup.html

Which 

[shaply](http://toblerity.github.com/shapely/manual.html)

> "The first premise of Shapely is that Python programmers should be able to perform PostGIS type geometry operations outside of an RDBMS."

Problem is very minimal reading/writing capabilities


KML/Json source: http://data.gent.be/categorie/grondgebied

* Direct KML 
* Direct JSON
* Converting to GeoJSON
* Converting to WKT


KML validation

    curl -O http://schemas.opengis.net/kml/2.2.0/atom-author-link.xsd
    curl -0 http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd
    xmllint --schema ogckml22.xsd sectoren.kml --noout


Goal: get sectors & wijken into Shapely for manipulations

1) WKT

ogr2ogr -f CSV wijken.csv wijken.kml -lco GEOMETRY=AS_WKT

ReadingError: Could not create geometry because of errors while reading input.  

# 

2) GeoJSON  

The JSON format provided by Ghent/Datatank is some custom format, i.e. not GeoJSON

Issues

lastkml will not 

the libkml driver that does support the ExtendedData should be included with GDAL starting from version 1.9.1. Unfortunately, the latest version obtainable for Ubuntu (PPA) for some reason does not come with libkml. As getting the full GDAL-stack to compile would likely lead to further yak-shaving, I abandonded that route. 

That leaves us with one non-reusable route: custom parsing (the elements contain typos etc.) the KML-attributes from the description element. a Python script that converts the KML to GeoJSON and reparses the KML to add the properties. 

Shaply provides needed operations

Reading in is tricky

JSON provided is 


