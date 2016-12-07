from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons

from google_api import *
from forms import *
from myapp import app, mail, UberCall

def Uber():
    dictstart = {}
    dictend={}

    global startLat,startLng,count,jsonarray,finalpath,test,midlength,startid,endId,sequence,endLat,endLng,endId,location
    count=0
    jsonarray = {}
    finalpath={}
    Query = Location.query.all()
    length = len(Query)

    #Fetching the data from database.
################################################################################################################
    for x in range(length):
        if Query[x].is_end_point==0 : # MId Queryints value
           dictmid={"lat":Query[x].lat,"lng":Query[x].lng,"id":Query[x].id}
           jsonarray[Query[x].id]=dictmid

        elif Query[x].is_end_point==1 :# Start points value
            startLat=str(Query[x].lat)
            startLng=str(Query[x].lng)
            startid=str(Query[x].id)

        else:                           # End points value
            endLat=str(Query[x].lat)
            endLng=str(Query[x].lng)
            endId=str(Query[x].id)
################################################################################################################

    print "jsonarray"+str(jsonarray)
    midL={}
    midlength=len(jsonarray)
    if(int(midlength) > 0 and int(midlength)!=1):

        while midlength > 1:
            print"Loop"+str(count)
            way={}
            for key in jsonarray.iteritems():
                lat=key[1]['lat']
                lng=key[1]['lng']
                id= key[1]['id']
                test=UberCall.ubercall(startLat,startLng,lat,lng)
                way[str(startid)+"-"+str(id)]=int(test)
                print "way="+str(way)
            minvalue=min(way, key=way.get)
            test=int(minvalue.split("-")[-1])
            print "test"+str(test)
            if test in jsonarray: del jsonarray[test]
            print jsonarray
            midlength=len(jsonarray)
            print "midlength"+str(midlength)
            Data=Location.query.filter_by(id=test).first()
            startLat=Data.lat
            startLng=Data.lng
            startid=Data.id
            print str(startLat)
            print str(startLng)
            count=count+1
            finalpath[count]=minvalue

        count=count+1
        finalpath[count]=str(test)+"-"+str(jsonarray.keys()[0])
        count=count+1
        finalpath[count]=str(jsonarray.keys()[0])+"-"+str(endId)
        print "Finalpath"+str(finalpath)
        test={}
        sequence=1
        for key in finalpath.iteritems():
            test[sequence]=str(key[1].split("-")[0])
            sequence=sequence+1
        location=0;
        for key in test.iteritems():
            FinalQuery=Location.query.filter_by(id=int(key[1])).first()
            midL[location]={'lat':FinalQuery.lat,'lon':FinalQuery.lng,'id':FinalQuery.id}
            location+=1

        midL[location]={'lat':endLat,'lon':endLng,'id':endId}
    elif(int(midlength)==1):
        print jsonarray.values()[0]['lat']
        midL[0]={'lat':startLat,'lon':startLng,'id':startid}
        midL[1]={'lat':jsonarray.values()[0]['lat'],'lon':jsonarray.values()[0]['lng'],'id':jsonarray.values()[0]['id']}
        midL[2]={'lat':endLat,'lon':endLng,'id':endId}
        print "json with One Location"+str(jsonarray)

    else:
        midL[0]={'lat':startLat,'lon':startLng,'id':startid}
        midL[1]={'lat':endLat,'lon':endLng,'id':endId}


    print "MIDDLE"+str(midL)

    #print "test"+str(test)
    #print "way"+str(way)
    print "jsonarray"+str(jsonarray)
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
    vari=len(midL)
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
        print "Data is coming or not"+ str(dataX)
        try:
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

        except:
            return "No Data Found"

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

    uberX['Price'] = str((add1 + add2) / 2)
    uberX['Time'] = str(float(addTime1 / 60))
    uberX['Miles'] = str(addDistance1)

    uberXL['Price'] = str((add1XL + add2XL) / 2)
    uberXL['Time'] = str(float(addTime2 / 60))
    uberXL['Miles'] = str(addDistance2)

    uberSLT['Price'] = str((add1Slt + add2Slt) / 2)
    uberSLT['Time'] = str(float(addTime3 / 60))
    uberSLT['Miles'] = str(addDistance3)

    uberBLK['Price'] = str((add1Blk + add2Blk) / 2)
    uberBLK['Time'] = str(float(addTime4 / 60))
    uberBLK['Miles'] = str(addDistance4)

    uberSUV['Price'] = str((add1SUV + add1SUV) / 2)
    uberSUV['Time'] = str(float(addTime5 / 60))
    uberSUV['Miles'] = str(addDistance5)

    ##
    print("UberX :"+uberX['Price']+uberSUV['Price'])
    ##
################################################################################################################
    if vari==0:
        final={'uberX':uberX,'uberXL':uberXL,'uberSelect':uberSLT,'uberBlack':uberBLK,'uberSUV':uberSUV}
    else:
        final = {'uberX': uberX, 'uberXL': uberXL, 'uberSelect': uberSLT, 'uberBlack': uberBLK, 'uberSUV': uberSUV,'OptimizedRoute': midL}
    print str(final)
    return final




