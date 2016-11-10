
# from flask_spyne import Spyne
#
# from spyne.protocol.json import JsonDocument
# from spyne.protocol.http import HttpRpc
# from spyne import Decimal, Unicode
# from flask import request
# from flask import json
#
# spyne = Spyne(app)
#
#
# class GoogleAPI(spyne.Service):
#     __service_url_path__ = ''
#     __in_protocol__ = HttpRpc(validator='soft')
#     __out_protocol__ = JsonDocument(ignore_wrappers=True)
#
#     name = ""
#     address = ""
#     city = ""
#     state = ""
#     zip = ""
#
#     def __init__(self, loc_name, loc_address, loc_city, loc_state, loc_zip):
#         self.name = loc_name
#         self.address = loc_address
#         self.city = loc_city
#         self.state = loc_state
#         self.zip = loc_zip
#
#     @spyne.srpc(Decimal, Decimal, Decimal, _returns=Unicode)
#     def process_data(lat, lon, radius):
#         # Get the information from the CrimeReport API
#         url = 'https://api.spotcrime.com/crimes.json'
#         params = {'lat': lat, 'lon': lon, 'radius': radius, 'key': '.'}
#         input_data = request.get(url=url, params=params)
#         input_json = json.loads(input_data.text)  # Convert response to JSON
#         return input_json
#         # Create the output_json

from myapp import app
from flask import json
import requests

class GoogleAPI(object):
    name = ""
    google_address = ""

    def __init__(self, loc_name, loc_address, loc_city, loc_state, loc_zip):
        self.name = loc_name
        self.process_data(loc_address, loc_city, loc_state, loc_zip)

    def process_data(self, loc_address, loc_city, loc_state, loc_zip):
        address = loc_address.replace (" ", "+")
        city = loc_city.replace(" ", "+")
        state = loc_state.replace(" ", "+")
        self.google_address = address + ",+" + city + ",+" + state

    def google(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': self.google_address, 'key': app.config["GOOGLE_KEY"]}
        input_data = requests.get(url=url, params=params)
        input_json = json.loads(input_data.text)  # Convert response to JSON
        return input_json
