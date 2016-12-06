from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons

from google_api import *
from forms import *
from myapp import app, mail, db

def Uber():
    jsonarray = []
    dictstart = {}
    dictend={}
    Query = Location.query.all()
    length = len(Query)
    print length

    #Fetching the data from database.
################################################################################################################
    for x in range(length):
        print jsonarray
        if Query[x].is_end_point==0 : # End points value
            jsonarray.append(Query[x].address+","+Query[x].city+","+Query[x].state+","+Query[x].zip)
            print "jsonarray"+str(jsonarray)

        elif Query[x].is_end_point==1 :# Start points value
            dictstart['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state+","+Query[x].zip
            startLat=Query[x].lat
            startLng=Query[x].lng
            print "dictstart="+str(dictstart)
        else:                           # Mid points value
            dictend['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state+","+Query[x].zip
            endLat=Query[x].lat
            endLng=Query[x].lng
            endDct = {"lat": endLat, "lon": endLng}
            print "dictend="+str(dictend)
################################################################################################################
    # If there are mid points between source and destination.
    # Google API Calling.
    # Work for Best route.

    if(len(jsonarray)!=0):

        URL = "https://maps.googleapis.com/maps/api/directions/json"
        origin1 = "origin=" + dictstart['Address']
        destination1 = "&destination=" + dictend['Address']
        dictmidlen=len(jsonarray)
        print "destination"+destination1
        print "source"+origin1
        test=""
        arr=[]
        for y in range(dictmidlen):
            test=test+"|"+jsonarray[y] ## Making the address as required in Google maps API.

        waypoints1 = "&waypoints=optimize:true" + test
        key1 = "&key=AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
        para = origin1 + destination1 + waypoints1 + key1
        req = requests.get(URL, params=para) # Requesting the data from Google maps API.
        d3 = req.json()
        way = d3["routes"][0]["waypoint_order"]
        waylength=len(way)
        fin=[]
        latitude=[]
        longitude=[]
        for x in range(waylength):
            Query=Location.query.filter_by(address=str(jsonarray[way[x]].split(",")[0])).first()
            latitude.append(Query.lat)
            longitude.append(Query.lng)

        mid1={}
        for x in range(waylength):
            mid1[x]={'lat':latitude[x],'lon':longitude[x]}

    # If there are no mid points between source and destination.
    else:
        mid1={}
################################################################################################################
    print("#######################################")
    # Uber API Pricing Calculations

    # URL of Uber API.
    URL = "https://api.uber.com/v1.2/estimates/price"
    # Header of Uber API.
    headers = {
        'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    midL={}
    # Providing Starting Value
    midL[0]={"lat":startLat,"lon":startLng}

    # Providing Mid points Values
    for y in range(len(mid1)):
        midL[y+1]=mid1[y]
    vari=len(midL)

    # Providing End Value
    midL[vari]={"lat": endLat, "lon": endLng}
    if vari==0:
        midL[1]={"lat": endLat, "lon": endLng}
    ####
    print midL
    print "mid Values"
    print midL
    print "Ended"

    print "Calculaion"
    ####


    maxLen = len(midL)
    counter = 0
    add1 = 0
    add2 = 0
    addTime1 = 0
    addDistance1 = 0
    flag=0 ####### Value of flag defined
    #uberXL
    addDistance2=0
    addTime2=0
    add1XL=0
    add2XL=0
    #uberSelect
    addDistance3=0
    addTime3=0
    add1Slt=0
    add2Slt=0
    #uberBlack
    addDistance4=0
    addTime4=0
    add1Blk=0
    add2Blk=0
    #uberSUV
    addDistance5=0
    addTime5=0
    add1SUV=0
    add2SUV=0
    # Calculation for uberX
    while counter < (maxLen - 1):
        sLat = midL.values()[counter].get('lat')
        sLon = midL.values()[counter].get('lon')
        eLat = midL.values()[counter + 1].get('lat')
        eLon = midL.values()[counter + 1].get('lon')
        paraX = {'start_latitude': sLat, 'start_longitude': sLon, 'end_latitude': eLat, 'end_longitude': eLon}
        rX = requests.get(URL, params=paraX, headers=headers)
        dataX = rX.json()
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

            elif it["localized_display_name"] == "uberXL":
                distanceX = it["distance"]
                addDistance2 = addDistance2 + distanceX
                timeX = it["duration"]
                addTime2 = addTime2 + timeX
                intX = it["estimate"]
                addX = intX.split("$")[-1]
                a1X = addX.split("-")[0]  # First Value
                add1XL = add1XL + int(a1X)
                a2X = addX.split("-")[-1]  # Second Value
                add2XL = add2XL + int(a2X)

            elif it["localized_display_name"] == "SELECT":
                distanceX = it["distance"]
                addDistance3 = addDistance3 + distanceX
                timeX = it["duration"]
                addTime3 = addTime3 + timeX
                intX = it["estimate"]
                addX = intX.split("$")[-1]
                a1X = addX.split("-")[0]  # First Value
                add1Slt = add1Slt + int(a1X)
                a2X = addX.split("-")[-1]  # Second Value
                add2Slt = add2Slt + int(a2X)

            elif it["localized_display_name"] == "BLACK":
                distanceX = it["distance"]
                addDistance4 = addDistance4 + distanceX
                timeX = it["duration"]
                addTime4 = addTime4 + timeX
                intX = it["estimate"]
                addX = intX.split("$")[-1]
                a1X = addX.split("-")[0]  # First Value
                add1Blk = add1Blk + int(a1X)
                a2X = addX.split("-")[-1]  # Second Value
                add2Blk = add2Blk + int(a2X)

            elif it["localized_display_name"] == "SUV":
                distanceX = it["distance"]
                addDistance5 = addDistance5 + distanceX
                timeX = it["duration"]
                addTime5 = addTime5 + timeX
                intX = it["estimate"]
                addX = intX.split("$")[-1]
                a1X = addX.split("-")[0]  # First Value
                add1SUV = add1SUV + int(a1X)
                a2X = addX.split("-")[-1]  # Second Value
                add2SUV = add2SUV + int(a2X)
        counter= counter+1

    uberX={}
    uberXL={}
    uberSLT={}
    uberBLK={}
    uberSUV={}
    uberX['Price'] = str(0)
    uberX['Time'] = str(0)
    uberX['Miles'] = str(0)
    uberXL['Price'] = str(0)
    uberXL['Time'] = str(0)
    uberXL['Miles'] = str(0)
    uberSLT['Price'] = str(0)
    uberSLT['Time'] = str(0)
    uberSLT['Miles'] = str(0)
    uberBLK['Price'] = str(0)
    uberBLK['Time'] = str(0)
    uberBLK['Miles'] = str(0)
    uberSUV['Price'] = str(0)
    uberSUV['Time'] = str(0)
    uberSUV['Miles'] = str(0)

    if flag != 1:

        uberX['Price'] = str((add1 + add2) / 2)
        uberX['Time'] = str(float(addTime1 / 60))
        uberX['Miles'] = str(addDistance1)

    if flag != 2:

        uberXL['Price'] = str((add1XL + add2XL) / 2)
        uberXL['Time'] = str(float(addTime2 / 60))
        uberXL['Miles'] = str(addDistance2)

    if flag != 3:

        uberSLT['Price'] = str((add1Slt + add2Slt) / 2)
        uberSLT['Time'] = str(float(addTime3 / 60))
        uberSLT['Miles'] = str(addDistance3)

    if flag != 4:

        uberBLK['Price'] = str((add1Blk + add2Blk) / 2)
        uberBLK['Time'] = str(float(addTime4 / 60))
        uberBLK['Miles'] = str(addDistance4)

    if flag != 5:

        uberSUV['Price'] = str((add1SUV + add1SUV) / 2)
        uberSUV['Time'] = str(float(addTime5 / 60))
        uberSUV['Miles'] = str(addDistance5)

    ##
    print("UberX :"+uberX['Price']+uberSUV['Price'])
    ##
################################################################################################################
    ########### Best Route ############

    route={}
    #route[0]=(dictstart['Address'].split(","))[0:4]
    route[0] = dictstart['Address']
    x=0
    cnt=len(jsonarray)
    while (cnt):
        #route[x+1]=(jsonarray[way[x]].split(","))[0:4]
        route[x+1]=jsonarray[way[x]] ##Taking the values from Google API's results.
        x=x+1
        cnt=cnt-1
    #route[len(jsonarray)+1]=(dictend['Address'].split(","))[0:4]
    route[len(jsonarray) + 1] = dictend['Address']
    ###
    print route
    print dataX["prices"]
    print len(dataX["prices"])
    ###
    # Returning the results to the calling object.

    if vari==0:
        final={'uberX':uberX,'uberXL':uberXL,'uberSelect':uberSLT,'uberBlack':uberBLK,'uberSUV':uberSUV}
    else:
        if flag == 1:
            final = {'uberX': 'No uberX data found', 'uberXL': uberXL, 'uberSelect': uberSLT, 'uberBlack': uberBLK,'uberSUV': uberSUV, 'OptimizedRoute': route}
        elif flag == 2:
            final = {'uberX': uberX, 'uberXL': 'No uberXL data found', 'uberSelect': uberSLT, 'uberBlack': uberBLK,'uberSUV': uberSUV, 'OptimizedRoute': route}
        elif flag == 3:
            final = {'uberX': uberX, 'uberXL': uberXL, 'uberSelect': 'No uberSelect data found', 'uberBlack': uberBLK,'uberSUV': uberSUV, 'OptimizedRoute': route}
        elif flag == 4:
            final = {'uberX': uberX, 'uberXL': uberXL, 'uberSelect': uberSLT, 'uberBlack': 'No uberBlack data found','uberSUV': uberSUV, 'OptimizedRoute': route}
        elif flag == 5:
            final = {'uberX': uberX, 'uberXL': uberXL, 'uberSelect': uberSLT, 'uberBlack': uberBLK,'uberSUV': 'No uberSUV data found', 'OptimizedRoute': route}
        else:
            final = {'uberX': uberX, 'uberXL': uberXL, 'uberSelect': uberSLT, 'uberBlack': uberBLK, 'uberSUV': uberSUV,'OptimizedRoute': route}
    return final




