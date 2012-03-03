import urllib2
from flask import Flask, jsonify, g
from gheocode import GhentGeoCoder

app = Flask(__name__)
@app.route("/")
def hello():
    return "gheocoding -- Ghent geocoder"

@app.route("/gheocode/<address_string>")
def return_geocoding(address_string):
    address_string = urllib2.unquote(address_string)
    g.G = GhentGeoCoder()

    return jsonify(g.G.gheocode(address_string))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
