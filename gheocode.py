import json, sys, redis
from pygeocoder import Geocoder, GeocoderError
from pyspatialite import dbapi2 as db

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

    def __init__(self, sqlitedb='gent.sqlite'):
        GeocodeCache.__init__(self)
        self.sqlitedb_name = sqlitedb

    def coord2areas(self, latitude, longitude):
        coords = (longitude, latitude)
        block_sql = "SELECT block_name, block_code FROM blocks WHERE ST_Contains(Geometry, MakePoint(%s,%s))" % coords
        sector_sql = "SELECT sector_name, sector_code FROM sectors WHERE ST_Contains(Geometry, MakePoint(%s,%s))" % coords


        conn = db.connect(self.sqlitedb_name)
        cur = conn.cursor()

        blockname, blockcode =  cur.execute(block_sql).fetchone()
        sectorname, sectorcode = cur.execute(sector_sql).fetchone()

        cur.close()
        conn.close()

        data = {'sector_name' : sectorname,
                'sector_code' : sectorcode,
                'block_name': blockname,
                'block_code' : blockcode }

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
            resp['geoinference_status'] = 'not within ghent'

        return resp

if __name__ == '__main__':
    G = GhentGeoCoder()
    addressstring = sys.argv[1]
    print G.gheocode(addressstring)
