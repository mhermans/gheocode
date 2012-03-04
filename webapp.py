import urllib2
from flask import Flask, jsonify
from gheocode import GhentGeoCoder

app = Flask(__name__)
@app.route("/")
def hello():
    return "gheocoding -- Ghent geocoder"

@app.route("/<address_string>")
def return_geocoding(address_string):
    address_string = urllib2.unquote(address_string)
    G = GhentGeoCoder()

    return jsonify(G.gheocode(address_string))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
