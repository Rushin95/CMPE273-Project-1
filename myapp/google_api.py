from myapp import app
from models import *
import requests

class GoogleAPI(object):
    google_address = ""

    user_id = 1   #If multiple users change it
    name = ""
    address = ""
    city =""
    state = ""
    zip = ""
    lat = ""
    lng = ""

    def __init__(self, name, address, city, state, zip):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.process_data()

    def process_data(self):
        address = self.address.replace(" ", "+")
        city = self.city.replace(" ", "+")
        state = self.state.replace(" ", "+")
        self.google_address = address + ",+" + city + ",+" + state

    def google(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': self.google_address, 'key': app.config["GOOGLEMAPS_KEY"]}
        details_resp = requests.get(url=url, params=params)
        details_json = details_resp.json()  # Convert response to JSON
        location = details_json['results'][0]['geometry']['location']
        self.lat = location['lat']
        self.lng = location['lng']
        coordinate = { 'lat': self.lat, 'lng': self.lng }
        #print(coordinate)
        self.addDB()
        return coordinate

    def addDB(self):
        newLocation = Location(self.user_id, self.name, self.address, self.city, self.state, self.zip, self.lat, self.lng)
        db.session.add(newLocation)
        db.session.commit()
