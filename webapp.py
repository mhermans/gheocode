import urllib2
from flask import Flask, jsonify
from gheocode import GhentGeoCoder

app = Flask(__name__)

@app.route("/")
def hello():
    return "gheocode -- geocoding for Ghent"

@app.route("/<address_string>")
def return_geocoding(address_string):
    address_string = urllib2.unquote(address_string)
    fn_wijken = 'geometries/geojson/wijken_extended.json'
    fn_sectoren = 'geometries/geojson/sectoren_extended.json'
    G = GhentGeoCoder(fn_wijken, fn_sectoren)

    return jsonify(G.gheocode(address_string))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=19922)
