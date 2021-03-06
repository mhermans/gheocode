# gheocode: geocoding for Ghent

## Overview

**gheocode** is a very simple wrapper around Google's geocoding service. But in addition to the regular latitude/longitude data and address normalisation, you get a small dash of geoinference. I.e. for each geocoded address in Ghent, you get the name and code of both the block and administrative sector the point is located in. To minimalise the load on Google's servers (you get a fixed amount of requests per day), responses are cached using a [Redis key-value store](http://redis.io/).

## Install

An example/testing service is running [here](http://service.mhermans.net/gheocode), but for heavier use then that, please use a local install. This should get you running:

    $ git clone git://github.com/mhermans/gheocode.git
    $ cd gheocode
    $ sudo apt-get install redis-server libgeos-c1
    $ pip install -r requirements.txt
    $ nosetests tests.py

## Running
    
    $ redis-server &
    $ python webapp.py

## Use

You can query the service with a simple GET-request containing the urlencoded address:

    $ curl http://service.mhermans.net/gheocode/korte%20Meer%203%209000%20Gent
    
    {
        "geocode_status": "OK", 
        "sector_code": "A02", 
        "number": "3", 
        "full_address": "Korte Meer 3, 9000 Ghent, Belgium", 
        "street": "Korte Meer", 
        "postal_code": "9000", 
        "lat": 51.0513082, 
        "query": "korte Meer 3 9000 Gent", 
        "geoinference_status": "OK", 
        "lng": 3.7228493, 
        "sector_name": "Kouter", 
        "country": "Belgium", 
        "locality": "Ghent", 
        "block_name": "Binnenstad", 
        "valid_address": true, 
        "block_code": "BIN"
    }

The service is most effectively used in combination with [Google Refine](http://code.google.com/p/google-refine/). Using the function "Add column by fetching URLs" on a column containing addresses in Ghent will pull in all the data in the form of [a JSON structure which you then can futher process](http://code.google.com/p/google-refine/wiki/FetchingURLsFromWebServices).

Use a GREL expression such as `'http://service.mhermans.net/gheocode/' + escape(value, 'url')` to fetch the data and `value.parseJson()["sector_code"]` to process the the resulting data into usable columns.

## Kudos

Uses open data [made available](http://data.gent.be/) by the city of Ghent. Runs on [Flask](http://flask.pocoo.org/), [shapely](http://toblerity.github.com/shapely/), [pygeocoder](https://bitbucket.org/xster/pygeocoder/wiki/Home) and [redis](http://redis.io/) + [bindings](https://github.com/andymccurdy/redis-py).
