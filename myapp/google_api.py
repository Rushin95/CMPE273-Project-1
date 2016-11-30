from myapp import app
from models import *
import requests

class GoogleAPI(object):
    google_address = ""
    user_id = 1   #If multiple users, then change it
    id = 0
    name = ""
    address = ""
    city =""
    state = ""
    zip = ""
    lat = ""
    lng = ""
    is_end_point = 0;

    def __init__(self, name, address, city, state, zip, is_end_point):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.is_end_point = is_end_point
        self.process_data()
        self.get_coordinates()
        self.addDB()

    def process_data(self):
        address = self.address.replace(" ", "+")
        city = self.city.replace(" ", "+")
        state = self.state.replace(" ", "+")
        self.google_address = address + ",+" + city + ",+" + state

    def get_coordinates(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': self.google_address, 'key': app.config["GOOGLEMAPS_KEY"]}
        details_resp = requests.get(url=url, params=params)
        details_json = details_resp.json()  # Convert response to JSON
        location = details_json['results'][0]['geometry']['location']
        self.lat = location['lat']
        self.lng = location['lng']
        #coordinate = { 'lat': self.lat, 'lng': self.lng }

    def addDB(self):
        newLocation = Location(self.user_id, self.name, self.address, self.city, self.state, self.zip, self.lat, self.lng, self.is_end_point)
        db.session.add(newLocation)
        db.session.commit()
        self.id = newLocation.id
