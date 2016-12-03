from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
from myapp import TestLyft
from myapp import app, mail, db  #import variables created in __init__.py

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')


######################

@app.route("/lyft", methods=['GET'])
def Lyft():
    test=TestLyft.Lyft()
    return str(test)

########################
@app.route("/test", methods=['GET'])
def Uber():
    x = 0
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
            #dictmid['Address'] = Query[x].address+","+Query[x].city+","+Query[x].state
            jsonarray.append(Query[x].address+","+Query[x].city+","+Query[x].state)
            print "jsonarray"+str(jsonarray)
        elif(Query[x].is_end_point==1):
            dictstart['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            print "dictstart="+str(dictstart)
        else:
            dictend['Address'] = Query[x].address + "," + Query[x].city + "," + Query[x].state
            print "dictend="+str(dictend)

    URL = "https://maps.googleapis.com/maps/api/directions/json"
    # params={"origin":{"Adelaide,SA"},"destination":{"Adelaide,SA"},"waypoints":{"optimize:true","Barossa+Valley,SA","Clare,SA","Connawarra,SA","McLaren+Vale,SA"},"key":{"AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"}}
    # params1="origin=Adelaide,SA&destination=Adelaide,SA&waypoints=optimize:true|Barossa+Valley,SA|Clare,SA|Connawarra,SA|McLaren+Vale,SA&key=AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
    origin1 = "origin=" + dictstart['Address']
    destination1 = "&destination=" + dictend['Address']
    dictmidlen=len(jsonarray)
    print "destination"+destination1
    print "source"+origin1
    test=""
    arr=[]
    for y in range(dictmidlen):
        test=test+"|"+jsonarray[y]
        #arr=arr+jsonarray[y]

    #return "hello"


    waypoints1 = "&waypoints=optimize:true" + test
    #waypoints1 = "&waypoints=optimize:true" + "|" + "Barossa+Valley,SA|" + "|" + "Clare,SA" + "|" + "Connawarra,SA" + "|" + "McLaren+Vale,SA"
    key1 = "AIzaSyDZIkQ6cFu5xz7se91BzMCN-Rs3Uhwfov4"
    para = origin1 + destination1 + waypoints1 + key1
    req = requests.get(URL, params=para)
    d3 = req.json()
    way = d3["routes"][0]["waypoint_order"]
    waylength=len(way)
    #str2 = str(way)
    #return str2
    fin=[]
    latitude=[]
    longitude=[]
    for x in range(waylength):
        Query=Location.query.filter_by(address=str(jsonarray[way[x]].split(",")[0])).first()
        latitude.append(Query.lat)
        longitude.append(Query.lng)


    '''
    se=jsonarray[0]
    dj=se.split(",")[0]
    print dj+se
    Query=Location.query.filter_by(address=str(dj)).first()
    x=Query.lat
    '''
    return str(latitude)

    headers = {
        'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    dic = {'A': {'lat': '37.334762', 'lon': '-121.907705'}, 'C1': {'lat': '37.335532', 'lon': '-121.885476'},
           'C': {'lat': '37.413477', 'lon': '-121.898105'}, 'D': {'lat': '37.383757', 'lon': '-121.886364'}}
    maxLen = len(dic)
    counter = 0
    add1 = 0
    add2 = 0
    addTime1 = 0
    addDistance1 = 0

    URL = "https://api.uber.com/v1.2/estimates/price"
    # Calculation for uberX
    while counter < (maxLen - 1):
        sLat = dic.values()[counter].get('lat')
        sLon = dic.values()[counter].get('lon')
        eLat = dic.values()[counter + 1].get('lat')
        eLon = dic.values()[counter + 1].get('lon')
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
        sLat = dic.values()[counter].get('lat')
        sLon = dic.values()[counter].get('lon')
        eLat = dic.values()[counter + 1].get('lat')
        eLon = dic.values()[counter + 1].get('lon')
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
    # t1=str(add2XL)
    printst1 = "Car Type uberX"
    printValue1 = "Total Estimated Price : " + "$" + str(add1) + " to " + "$" + str(add2)
    printTime1 = "Total Estimated time in minutes : " + str(float(addTime1 / 60))
    printDistance1 = "Total Distance in Miles : " + str(addDistance1)

    printst2 = "Car Type uberXL"
    printValue2 = "Total Estimated Price : " + "$" + str(add1XL) + " to " + "$" + str(add2XL)
    printTime2 = "Total Estimated time in minutes : " + str(float(addTime2 / 60))
    printDistance2 = "Total Distance in Miles : " + str(addDistance2)

    print1 = printst1 + "\n" + printValue1 + "\n" + printTime1 + "\n" + printDistance1 + "\n" + "\n" + printst2 + "\n" + printValue2 + "\n" + printTime2 + "\n" + printDistance2
    # return print1


########################

@app.route('/addplaces',methods=['GET'])
def addplaces():
    x=0
    jsonarray=[]
    dict={}
    dict2={}

    Query=Location.query.all()
    length=len(Query)
    print length
    for x in range(length):
        print jsonarray
        dict['uid']=Query[x].id
        dict['address']=Query[x].address
        dict['city']=Query[x].city
        dict['state']=Query[x].state
        dict['zip']=Query[x].zip
        dict['is_end_point']=Query[x].is_end_point
        jsonarray.append(dict.copy())
    return render_template('addplaces.html',data=jsonarray,length=length)

@app.route('/deleteaddress',methods=['GET', 'POST','Delete'])
def deleteadd():
    uid=request.form.get('x')
    Delete_data=Location.query.filter_by(id=uid).first()
    endpt=Delete_data.is_end_point
    if(endpt==1 or endpt==2):
        flash('Cannot Delete End Points')
        return redirect('/addplaces')
    else:
        db.session.delete(Delete_data)
        db.session.commit()
        return redirect('/addplaces')

@app.route('/about')
def about():
    fake_user = {'nickname': 'Juancho'}
    return render_template('about.html', title='About', user=fake_user)    #You can put these attributes on the templates

@app.route('/faq')
def faq():
    fake_questions = [  # fake array of questions
        {
            'author': {'nickname': 'John'},
            'body': 'How does Flask work?!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'How integrate with SQLAlchemy?'
        }
    ]
    return render_template('faq.html', title='FAQ', user='client', questions=fake_questions)


@app.route('/places', methods=['GET', 'POST'])
def places():
    form = PlacesForm()

    # Create a User by default
    if not User.query.get(1):
        newuser = User("", "", "", "")
        db.session.add(newuser)
        db.session.commit()

    my_markers = { icons.dots.green: [], icons.dots.red: [] }

    # Import markers from Locations on DB
    end_points = 0
    locations = Location.query.all()
    for loc in locations:
        lat = loc.lat
        lng = loc.lng
        point_info = loc.address + ", " + loc.city + ", " + loc.state + ", " + unicode(loc.zip)
        point = (lat, lng, point_info)
        if(loc.is_end_point==1 or loc.is_end_point==2):  #point is at start or end
            if loc.is_end_point==1:
                form.Endpoint.choices = [('0', 'Other'), ('2', 'End')]
            elif loc.is_end_point==2:
                form.Endpoint.choices = [('0', 'Other'), ('1', 'Start')]
            my_markers[icons.dots.red].append(point)
            end_points+=1
        else:
            my_markers[icons.dots.green].append(point)

    if request.method == 'POST':        #capture the form field data and check if it's valid
        if form.validate():
            #Get the Address from TextBox
            data = [x.strip() for x in form.Gaddress.data.split(',')]
            #If invalid Address Format
            if len(data) != 5:
                flash('Invalid Address format. Allowed Format: Street Address, City, State, Country, Zipcode')
                mymap = Map(identifier="mymap", varname="mymap", lat=app.config['LAT'], lng=app.config['LNG'],
                            style="width:400px;height:400px;margin:50;", markers=my_markers, zoom=9)
                return render_template('places.html', title='Places', form=form, mymap=mymap, end_points=end_points)

            #Get latitude and longitude and Store point into the DB
            location = GoogleAPI(form.name.data, data[0], data[1], data[2], data[4], int(form.Endpoint.data))

            #Add point to the map
            point_info = location.address + ", " + location.city + ", " + location.state + ", " + location.zip
            point = (location.lat, location.lng, point_info)
            my_markers[icons.dots.green].append(point)

            # After a Valid Form is fill ALWAYS USE redirect
            return redirect(url_for('places'))
        else:
            flash('All fields are required.')
            mymap = Map(identifier="mymap", varname="mymap", lat=app.config['LAT'], lng=app.config['LNG'],
                        style="width:400px;height:400px;margin:50;", markers=my_markers, zoom=9)
            # initial GET or INVALID form use render_template
            return render_template('places.html', title='Places', form=form, mymap=mymap, end_points=end_points)

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
        # Create Map after have the markers defined. Cuase it put markers only when create map object
        # identifier for DOM element, varname for JS object name
        mymap = Map(identifier="mymap", varname="mymap", lat=app.config['LAT'], lng=app.config['LNG'],
                    style="width:400px;height:400px;margin:50;", markers=my_markers, zoom=9)
        # initial GET use render_template
        return render_template('places.html', title='Places', form=form, mymap=mymap, end_points=end_points)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate():
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            print('Record was successfully added')
            # Send the message
            msg = Message('New Location', sender='loco_perro@rocketmail.com',
                          recipients=['loco_perro@rocketmail.com', 'juankpapi@hotmail.com'])
            message_route = 'The best cost based route is: '
            msg.body = """
                              From: %s <%s>
                              %s
                              """ % (form.firstname.data, form.email.data, message_route)
            mail.send(msg)
            print('Message sent')

            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
        else:
            flash('All fields are required.')
            return render_template('signup.html', title='Sign Up', form=form)

    elif request.method == 'GET':
        return render_template('signup.html', title='Sign Up', form=form)


#=========================================
#RESTful
@app.route('/locations', methods=['POST'])
def locations_POST():
    if request.method == 'POST':
        # Create a User by default
        if not User.query.get(1):
            newuser = User("", "", "", "")
            db.session.add(newuser)
            db.session.commit()

        # Get the data from Request Body
        request_data = json.loads(request.data)

        location_type = 0  #by default=0
        # Get latitude and longitude and Store point into the DB
        location = GoogleAPI(request_data['name'], request_data['address'], request_data['city'], request_data['state'], request_data['zip'], location_type)

        # Create the response's data
        data = {
            "id": str(location.id),
            "name": location.name,
            "address": location.address,
            "city": location.city,
            "state": location.state,
            "zip": location.zip,
            "coordinate": {
                "lat": location.lat,
                "lng": location.lng
            }
        }
        # Creates the response
        return make_response(json.dumps(data), 201)


@app.route('/locations/<location_id>', methods=['GET'])
def locations_GET(location_id):
    if request.method == 'GET':
        location = Location.query.get(location_id)
        if location is not None:
            #Create the response's data from DB
            data = {
                "id": str(location.id),
                "name": location.name,
                "address": location.address,
                "city": location.city,
                "state": location.state,
                "zip": location.zip,
                "coordinate": {
                    "lat": location.lat,
                    "lng": location.lng
                }
            }
            return make_response(json.dumps(data), 200)
        else:
            data = ""
            return make_response(json.dumps(data), 404)

@app.route('/locations/<location_id>', methods=['PUT'])
def locations_PUT(location_id):
    if request.method == 'PUT':
        # Get the data from Request Body
        request_data = json.loads(request.data)

        if (not request_data['name']):
            print('Please enter <name>', 'error')
        else:
            location = Location.query.get(location_id)
            if location is not None:
                location.name = request_data['name']
                db.session.commit()

            # Creates the response
            data = ""
            return make_response(json.dumps(data), 202)


@app.route('/locations/<location_id>', methods=['DELETE'])
def locations_DELETE(location_id):
    if request.method == 'DELETE':
        location = Location.query.get(location_id)
        if location is not None:
            db.session.delete(location)
            db.session.commit()

        # Creates the response
        data = ""
        return make_response(json.dumps(data), 204)
