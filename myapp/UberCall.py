from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
import pdfkit
from myapp import TestLyft
from myapp import GetMin
from myapp import app, mail, db  #import variables created in __init__.py
import json

def ubercall(sLat,sLon,eLat,eLon):

    # URL of Uber API.
    URL = "https://api.uber.com/v1.2/estimates/price"
    # Header of Uber API.
    headers = {
        'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    paraX = {'start_latitude': sLat, 'start_longitude': sLon, 'end_latitude': eLat, 'end_longitude': eLon}
    rX = requests.get(URL, params=paraX, headers=headers)
    dataX = rX.json()
    addDistance1=0
    addTime1=0
    add1=0
    add2=0
    for it in dataX["prices"]:
            if it["localized_display_name"] == "uberX":
                distanceX = it["distance"]
                addDistance1 = addDistance1 + distanceX
                timeX = it["duration"]
                addTime1 = addTime1 + timeX
                intX = it["estimate"]
                addX = intX.split("$")[-1]
                a1X = addX.split("-")[0]  # First Value
                add1 = add1 + int(a1X)
                a2X = addX.split("-")[-1]  # Second Value
                add2 = add2 + int(a2X)
                final=((add1+add2)/2)
    return str(final)
