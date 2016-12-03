from flask import Flask
from flask import jsonify
import requests
import json

app = Flask(__name__)

@app.route("/",methods=['GET'])
def Uber():
    AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4

    URL="https://maps.googleapis.com/maps/api/directions/json"
    places={"optimize:true","Barossa+Valley,SA","Clare,SA","Connawarra,SA","McLaren+Vale,SA"}
    origin1={"Adelaide,SA"}
    destination1={"Adelaide,SA"}
    key1=AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4

    req=requests.get(URL,origin=origin1,destination=destination1,waypoints=places,key=key1)
    d3=req.json()
    way=d3["routes"]["waypoint_order"]
    return way

    headers = {
            'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/json',
        }
    dic={'A':{'lat':'37.334762', 'lon':'-121.907705'},'C1':{'lat':'37.335532', 'lon':'-121.885476'},'C':{'lat':'37.413477', 'lon':'-121.898105'},'D':{'lat':'37.383757', 'lon':'-121.886364'}}
    maxLen=len(dic)
    counter=0
    add1=0
    add2=0

    URL="https://api.uber.com/v1.2/estimates/price"
    #Calculation for uberX
    while counter<(maxLen-1):
        sLat=dic.values()[counter].get('lat')
        sLon=dic.values()[counter].get('lon')
        eLat=dic.values()[counter+1].get('lat')
        eLon=dic.values()[counter+1].get('lon')
        paraX={'start_latitude':sLat,'start_longitude':sLon,'end_latitude':eLat,'end_longitude':eLon}
        rX = requests.get(URL,params=paraX,headers=headers)
        dataX=rX.json()
        intX=dataX["prices"][1]["estimate"]
        addX=intX.split("$")[-1]
        a1X=addX.split("-")[0]#First Value
        add1=add1+int(a1X)
        a2X=addX.split("-")[-1]#Second Value
        add2=add2+int(a2X)
        counter +=1
    
    counter=0
    add1XL=0
    add2XL=0
    #Calculation for uberXL
    while counter<(maxLen-1):
        sLat=dic.values()[counter].get('lat')
        sLon=dic.values()[counter].get('lon')
        eLat=dic.values()[counter+1].get('lat')
        eLon=dic.values()[counter+1].get('lon')
        paraX={'start_latitude':sLat,'start_longitude':sLon,'end_latitude':eLat,'end_longitude':eLon}
        rX = requests.get(URL,params=paraX,headers=headers)
        dataX=rX.json()
        intX=dataX["prices"][2]["estimate"]
        addX=intX.split("$")[-1]
        a1X=addX.split("-")[0]#First Value
        add1XL=add1XL+int(a1X)
        a2X=addX.split("-")[-1]#Second Value
        add2XL=add1XL+int(a2X)
        counter +=1
    #t1=str(add2XL)
    print1= "Total Estimated Price for uberX : "+"$"+str(add1)+" to "+"$"+str(add2)
    print2= "Total Estimated Price for uberXL : "+"$"+str(add1XL)+" to "+"$"+str(add2XL)
    #return print1+"\n"+print2

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)