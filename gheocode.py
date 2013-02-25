import json, sys, redis
from pygeocoder import Geocoder, GeocoderError
#from pyspatialite import dbapi2 as db
from shapely.geometry import Point, shape

class GeocodeCache(object):
    """Wrapper for Google geocoding, cached by Redis."""

    def __init__(self, redisuri=None):
        # TODO: accept config-URI instead of harcoded
        self.redis = redis.Redis('localhost', 6379, 0)

        # check if Redis is running
        try:
            self.redis.info()
            self.redis_online = True
        except redis.exceptions.ConnectionError:
            self.redis_online = False

    def geocode(self, address_string):

        data = {}

        if self.redis_online:
            data = self.redis.hgetall(address_string)

        if not data:
            try:
                #TODO multiple results?
                result = Geocoder.geocode(address_string)[0]
            except GeocoderError:
                result = None

            if result:
                data = {}
                data['valid_address'] = result.valid_address
                data['full_address'] = result.formatted_address
                data['country'] = result.country
                data['postal_code'] = result.postal_code
                data['locality'] = result.locality
                data['street'] = result.route
                data['number'] = result.street_number
                data['lat'], data['lng'] = result.coordinates
                data['raw'] = json.dumps(result.raw)

                self.redis.hmset(address_string, data)

            else:
                data = None

        return data


class GhentGeoCoder(GeocodeCache):

    def __init__(self, fn_wijken, fn_sectoren):
        GeocodeCache.__init__(self)
        #self.sqlitedb_name = sqlitedb

        # load geojson for wijken, sectoren + insert shapely geometries
        with open(fn_wijken, 'r') as f:
            self.wijken = json.load(f)['features']
        for wijk in self.wijken:
            wijk['polygon'] = shape(wijk['geometry'])

        with open(fn_sectoren, 'r') as f:
            self.sectoren = json.load(f)['features']
        for sector in self.sectoren:
            sector['polygon'] = shape(sector['geometry'])

    def get_wijk(self, point):
        for wijk in self.wijken:
            if wijk['polygon'].intersects(point):
                return wijk

    def get_sector(self, point):
        for sector in self.sectoren:
            if sector['polygon'].intersects(point):
                return sector

    def coord2areas(self, latitude, longitude):
        point = Point(float(longitude), float(latitude))
        wijk = self.get_wijk(point)
        sector = self.get_sector(point)

        if not wijk and sector: 
            return {}

        data = {'sector_name' : sector['properties']['sectornaam'],
                'sector_code' : sector['properties']['sectorcode'],
                'block_name': wijk['properties']['wijk'],
                'block_code' : wijk['properties']['wijknr'] }

        return data

    def gheocode(self, address_string):
        resp = {'query' : address_string }


        try:
            resp.update(self.geocode(address_string))
            del resp['raw'] # not interested in raw results
            resp['geocode_status'] = 'OK'

        except TypeError:
            resp['geocode_status'] = 'invalid address'
            return resp

        try:
            area_data = self.coord2areas(resp['lat'], resp['lng'])
            resp.update(area_data)
            resp['geoinference_status'] = 'OK'

        except TypeError:
            resp['geoinference_status'] = 'not within Ghent'

        return resp

if __name__ == '__main__':
    fn_wijken = 'geometries/geojson/wijken_extended.json'
    fn_sectoren = 'geometries/geojson/sectoren_extended.json'
    G = GhentGeoCoder(fn_wijken, fn_sectoren)
    addressstring = sys.argv[1]
    print G.gheocode(addressstring)
