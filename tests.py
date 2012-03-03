from gheocode import GhentGeoCoder

def test_valid_ghent_address():
    G = GhentGeoCoder()
    r = G.gheocode("Tijgerstraat 9 Gent")
    assert r['sector_code'] == u'A24'
    assert r['lng'] ==  '3.7308366'
    assert r['sector_name'] == u'Dierentuin'
    assert r['full_address'] ==  'Tijgerstraat 9, 9000 Ghent, Belgium'
    assert r['geocode_status'] == r['geoinference_status'] == 'OK'

def test_outside_address():
    G = GhentGeoCoder()
    r = G.gheocode("Alfons Gossetlaan 30 Groot-bijgaarden")
    print r
    assert r['full_address'] == 'Gosset, Alfons Gossetlaan 30, 1702 Dilbeek, Belgium'
    assert r['geoinference_status'] == 'not within ghent'
    assert r['geocode_status'] == 'OK'

def test_invalid_addres():
    G = GhentGeoCoder()
    r = G.gheocode('Demerstraat 23 3200 Bierbeek')
    assert r['geocode_status'] == 'invalid address'
