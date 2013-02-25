#! /usr/bin/env python
import json
from lxml import etree

# INSERT KML EXTENDED DATA ATTRIBUTES INTO GEOJSON
# ------------------------------------------------


def _parse_wijk_description(data):
    data = '<data>' + data + '</data>'
    data = etree.fromstring(data)
    d = {}
    d['id'] = data.find('id').text
    d['naam'] = data.find('naam').text
    d['wijk'] = data.find('wijk').text
    d['wijknr'] = data.find('wijknr').text

    return d

def _parse_sector_description(data):
    data = '<data>' + data + '</data>'
    data = etree.fromstring(data)
    d = {}
    d['id'] = data.find('id').text
    d['fid'] = data.find('fid').text
    d['statsec_id'] = data.find('statsec_id').text
    d['sectorcode'] = data.find('sectorcode').text
    d['sectornaam'] = data.find('sectornaam').text
    d['stadcode'] = data.find('stadcode').text
    d['wijknr'] = data.find('wijknr').text
    d['objectid'] = data.find('objectid').text
    d['area'] = data.find('area').text

    return d


def add_extended_data(geojson, feature_type):
    for feature in geojson['features']:
        # extendeddata is not preserved, need to parse from xml in description
        if feature_type == 'wijk':
            data = _parse_wijk_description(feature['properties']['Description'])
        if feature_type == 'sector':
            data = _parse_sector_description(feature['properties']['Description'])

        feature['properties'].update(data)

    return geojson

def update_properties(fn_in, fn_out, feature_type):
    with open(fn_in, 'r') as f:
        js = json.load(f)

    js = add_extended_data(js, feature_type)
    pprint.pprint(js)

    with open(fn_out, 'w') as f:
        json.dump(js, f, indent=4)

if __name__ == '__main__':
    update_properties('wijken.json', 'wijken_extended.json', 'wijk')
    update_properties('sectoren.json', 'sectoren_extended.json', 'sector')
