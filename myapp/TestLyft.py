from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
from myapp import app, mail, db
def Lyft(Query):
    jsonarray = []
    dictstart = {}
    dictend={}
    length = len(Query)
    print length
    for x in range(length):
        print jsonarray
        if(Query[x].is_end_point==0):
            #dictmid['Address'] = Query[x].address+","+Query[x].city+","+Query[x].state
            jsonarray.append(Query[x].address+","+Query[x].city+","+Query[x].state)
            print "jsonarray"+str(jsonarray)
        elif(Query[x].is_end_point==1):
            dictstart['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            source_string = ','+ str(Query[x].lat)+ ',' + str(Query[x].lng)
            print "dictstart="+str(dictstart)
        else:
            dictend['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            print "dictend="+str(dictend)
            destination_string = ','+ str(Query[x].lat)+ ',' + str(Query[x].lng)

    URL = "https://maps.googleapis.com/maps/api/directions/json"
    # params={"origin":{"Adelaide,SA"},"destination":{"Adelaide,SA"},"waypoints":{"optimize:true","Barossa+Valley,SA","Clare,SA","Connawarra,SA","McLaren+Vale,SA"},"key":{"AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"}}
    # params1="origin=Adelaide,SA&destination=Adelaide,SA&waypoints=optimize:true|Barossa+Valley,SA|Clare,SA|Connawarra,SA|McLaren+Vale,SA&key=AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
    origin1 = "origin=" + dictstart['Address']
    destination1 = "&destination=" + dictend['Address']
    dictmidlen=len(jsonarray)
    print "destination"+destination1
    print "source"+origin1
    test=""
    for y in range(dictmidlen):
        test=test+"|"+jsonarray[y]

    waypoints1 = "&waypoints=optimize:true" + test
    #waypoints1 = "&waypoints=optimize:true" + "|" + "Barossa+Valley,SA|" + "|" + "Clare,SA" + "|" + "Connawarra,SA" + "|" + "McLaren+Vale,SA"
    key1 = "AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
    para = origin1 + destination1 + waypoints1 + key1
    req = requests.get(URL, params=para)
    d3 = req.json()
    way = d3["routes"][0]["waypoint_order"]
    waylength=len(way)

    latitude=[]
    longitude=[]
    strng= str(waylength + 2)+source_string

    for x in range(waylength):
        Query=Location.query.filter_by(address=str(jsonarray[way[x]].split(",")[0])).first()
        latitude.append(Query.lat)
        longitude.append(Query.lng)
        strng += ','+ str(Query.lat) +','+ str(Query.lng)
        print strng
        print 'insideloop'
        # return pstring
    strng += destination_string
    print strng

    # lyft api logic
    lat = []
    lng = []
    cords = strng.split(',')
    # fetching the no of locations to be covered
    no_of_cords = int(cords[0])
    count = 0
    # yield len(cords)
    # yield cords[0]

    # setting the lat and lng list from the string given as a parameter
    while count < no_of_cords:
        lat.append(cords[(2 * count) + 1])
        lng.append(cords[(2 * count) + 2])

        count += 1

    # dictionary for each type of ride
    lyft = {'min_cost': 0,
            'max_cost': 0,
            'time': 0,
            'distance': 0,
            'type': 'lyft'
            }
    lyft_line = {'min_cost': 0,
                 'max_cost': 0,
                 'time': 0,
                 'distance': 0,
                 'type': 'lyft_line'

                 }
    lyft_plus = {'min_cost': 0,
                 'max_cost': 0,
                 'time': 0,
                 'distance': 0,
                 'type': 'lyft_plus'
                 }
    lyft_premier = {'min_cost': 0,
                    'max_cost': 0,
                    'time': 0,
                    'distance': 0,
                    'type': 'lyft_premier'
                    }
    cheapest = {
        'cost': 0,
        'distance': 0,
        'time': 0,
        'type': ''
    }

    # making call for ride between each 2 sets of (lat,lng)
    count = 0
    while count != (no_of_cords - 1):

        payload = {'start_lat': lat[count], 'start_lng': lng[count], 'end_lat': lat[count + 1],
                   'end_lng': lng[count + 1]}
        headers = {
            'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/json',
        }

        stop = requests.get(
            'https://api.lyft.com/v1/cost?',
            headers=headers, params=payload)
        print stop.json()
        result = stop.json()
        count += 1

        # assigning values in the dictionary
        for iteration in result["cost_estimates"]:
            if iteration["ride_type"] == "lyft_plus":
                lyft_plus["min_cost"] += iteration["estimated_cost_cents_min"]
                lyft_plus["max_cost"] += iteration["estimated_cost_cents_max"]
                lyft_plus["time"] += iteration["estimated_duration_seconds"]
                lyft_plus["distance"] += iteration["estimated_distance_miles"]
                # yield lyft_plus

            elif iteration["ride_type"] == "lyft_line":
                lyft_line["min_cost"] += iteration["estimated_cost_cents_min"]
                lyft_line["max_cost"] += iteration["estimated_cost_cents_max"]
                lyft_line["time"] += iteration["estimated_duration_seconds"]
                lyft_line["distance"] += iteration["estimated_distance_miles"]
                # yield lyft_line

            elif iteration["ride_type"] == "lyft":
                lyft["min_cost"] += iteration["estimated_cost_cents_min"]
                lyft["max_cost"] += iteration["estimated_cost_cents_max"]
                lyft["time"] += iteration["estimated_duration_seconds"]
                lyft["distance"] += iteration["estimated_distance_miles"]
                # yield lyft

            elif iteration["ride_type"] == "lyft_premier":
                lyft_premier["min_cost"] = iteration["estimated_cost_cents_min"]
                lyft_premier["max_cost"] = iteration["estimated_cost_cents_max"]
                lyft_premier["time"] = iteration["estimated_duration_seconds"]
                lyft_premier["distance"] = iteration["estimated_distance_miles"]
                # yield lyft_premier
    cheapest['cost'] = lyft_line['min_cost']
    if (lyft_premier['max_cost'] != 0 and lyft_premier['min_cost'] < cheapest['cost']):
        cheapest['cost'] = lyft_premier['min_cost']
        cheapest['time'] = lyft_premier['time']
        cheapest['distance'] = lyft_premier['distance']
        cheapest['type'] = lyft_premier['type']

    if (lyft_plus['max_cost'] != 0 and lyft_plus['min_cost'] < cheapest['cost']):
        cheapest['cost'] = lyft_plus['min_cost']
        cheapest['time'] = lyft_plus['time']
        cheapest['distance'] = lyft_plus['distance']
        cheapest['type'] = lyft_plus['type']
    if (lyft['max_cost'] != 0 and lyft['min_cost'] < cheapest['cost']):
        cheapest['cost'] = lyft['min_cost']
        cheapest['time'] = lyft['time']
        cheapest['distance'] = lyft['distance']
        cheapest['type'] = lyft['type']

    if (lyft_line['min_cost'] != 0 and lyft_premier['min_cost'] < cheapest['cost']):
        cheapest['cost'] = lyft_line['min_cost']
        cheapest['time'] = lyft_line['time']
        cheapest['distance'] = lyft_line['distance']
        cheapest['type'] = lyft_line['type']

    print "FULL TRIP STATISTICS"
    print "For lyft:", lyft
    print "For lyft_line:", lyft_line
    print "For lyft_plus:", lyft_plus
    print "For lyft_premier:", lyft_premier
    print 'Cheapest:', cheapest
    all={'lyft':lyft,'lyft_line':lyft_line,'lyft_plus':lyft_plus,'lyft_premier':lyft_premier}
    return all
