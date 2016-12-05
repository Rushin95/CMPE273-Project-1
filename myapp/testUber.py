from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons

from google_api import *
from forms import *
from myapp import app, mail, db

def Uber():
    jsonarray = []
    dictmid = {}
    dictstart = {}
    dictend={}
    Query = Location.query.all()
    length = len(Query)
    print length
    for x in range(length):
        print jsonarray
        if(Query[x].is_end_point==0):
            jsonarray.append(Query[x].address+","+Query[x].city+","+Query[x].state)
            print "jsonarray"+str(jsonarray)
        elif(Query[x].is_end_point==1):

            dictstart['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            startLat=Query[x].lat
            startLng=Query[x].lng
            print "dictstart="+str(dictstart)
        else:
            dictend['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            endLat=Query[x].lat
            endLng=Query[x].lng
            endDct = {"lat": endLat, "lon": endLng}
            print "dictend="+str(dictend)
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
            test=test+"|"+jsonarray[y]


        waypoints1 = "&waypoints=optimize:true" + test
        key1 = "AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
        para = origin1 + destination1 + waypoints1 + key1
        req = requests.get(URL, params=para)
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

        st1=[]
        en=[]
        print Location.query.filter_by(address=str(dictstart['Address'])).first()
        startLoc={'lat':startLat,'lon':startLng}
        st1.append(startLoc)
        endLoc={'lat':endLat,'lon':endLng}
        en.append(endLoc)
        mid1={}
        for x in range(waylength):
            mid1[x]={'lat':latitude[x],'lon':longitude[x]}
    else:
        mid1={}

    print("#######################################")
    headers = {
        'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    midL={}
    midL[0]={"lat":startLat,"lon":startLng}
    for y in range(len(mid1)):
        midL[y+1]=mid1[y]
    vari=len(midL)
    midL[vari]={"lat": endLat, "lon": endLng}
    if vari==0:
        midL[1]={"lat": endLat, "lon": endLng}
    print midL
    print "mid Values"
    print midL
    print "Ended"

    maxLen = len(midL)
    counter = 0
    add1 = 0
    add2 = 0
    addTime1 = 0
    addDistance1 = 0
    print "Calculaion"
    URL = "https://api.uber.com/v1.2/estimates/price"
    # Calculation for uberX
    while counter < (maxLen - 1):
        sLat = midL.values()[counter].get('lat')
        sLon = midL.values()[counter].get('lon')
        eLat = midL.values()[counter + 1].get('lat')
        eLon = midL.values()[counter + 1].get('lon')
        paraX = {'start_latitude': sLat, 'start_longitude': sLon, 'end_latitude': eLat, 'end_longitude': eLon}
        rX = requests.get(URL, params=paraX, headers=headers)
        dataX = rX.json()
        distanceX = dataX["prices"][1]["distance"]
        addDistance1 = addDistance1 + distanceX
        timeX = dataX["prices"][1]["duration"]
        addTime1 = addTime1 + timeX
        intX = dataX["prices"][1]["estimate"]
        addX = intX.split("$")[-1]
        a1X = addX.split("-")[0]  # First Value
        add1 = add1 + int(a1X)
        a2X = addX.split("-")[-1]  # Second Value
        add2 = add2 + int(a2X)
        counter += 1

    counter = 0
    add1XL = 0
    add2XL = 0
    addTime2 = 0
    addDistance2 = 0
    # Calculation for uberXL
    while counter < (maxLen - 1):
        sLat = midL.values()[counter].get('lat')
        sLon = midL.values()[counter].get('lon')
        eLat = midL.values()[counter + 1].get('lat')
        eLon = midL.values()[counter + 1].get('lon')
        paraX = {'start_latitude': sLat, 'start_longitude': sLon, 'end_latitude': eLat, 'end_longitude': eLon}
        rX = requests.get(URL, params=paraX, headers=headers)
        dataX = rX.json()
        distanceX = dataX["prices"][1]["distance"]
        addDistance2 = addDistance2 + distanceX
        timeX = dataX["prices"][2]["duration"]
        addTime2 = addTime2 + timeX
        intX = dataX["prices"][2]["estimate"]
        addX = intX.split("$")[-1]
        a1X = addX.split("-")[0]  # First Value
        add1XL = add1XL + int(a1X)
        a2X = addX.split("-")[-1]  # Second Value
        add2XL = add1XL + int(a2X)
        counter += 1

    printst1 = "Car Type uberX"
    printValue1 = "Total Estimated Price : " + "$" + str(add1) + " to " + "$" + str(add2)
    printTime1 = "Total Estimated time in minutes : " + str(float(addTime1 / 60))
    printDistance1 = "Total Distance in Miles : " + str(addDistance1)

    printst2 = "Car Type uberXL"
    printValue2 = "Total Estimated Price : " + "$" + str(add1XL) + " to " + "$" + str(add2XL)
    printTime2 = "Total Estimated time in minutes : " + str(float(addTime2 / 60))
    printDistance2 = "Total Distance in Miles : " + str(addDistance2)
    uberX={}
    uberXL={}
    print1 = printst1 + "\n" + printValue1 + "\n" + printTime1 + "\n" + printDistance1 + "\n" + "\n" + printst2 + "\n" + printValue2 + "\n" + printTime2 + "\n" + printDistance2
    uberX['Price']=str((add1+add2)/2)
    uberX['Time']=str(float(addTime1 / 60))
    uberX['Miles']=str(addDistance1)
    uberXL['Price']=str((add1XL+add2XL)/2)
    uberXL['Time']=str(float(addTime2 / 60))
    uberXL['Miles']=str(addDistance2)
    print("UberX :"+uberX['Price'])
    ########### Best Route ############
    route={}
    route[0]=(dictstart['Address'].split(","))[0:2]
    print route
    x=0
    cnt=len(jsonarray)
    while (cnt):
        route[x+1]=(jsonarray[way[x]].split(","))[0:2]
        x=x+1
        cnt=cnt-1
    route[len(jsonarray)+1]=(dictend['Address'].split(","))[0:2]
    print route

    final={'uberX':uberX,'uberXL':uberXL,'Optimized Route':route}
    if vari==0:
        final={'uberX':uberX,'uberXL':uberXL}
    return final


