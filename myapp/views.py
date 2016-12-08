from flask import render_template, redirect, request, flash, url_for, json, make_response, session
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
import pdfkit
from myapp import TestLyft
from myapp import UberCall
from myapp import testUber
from myapp import GetMin
from myapp import app, mail, db  #import variables created in __init__.py
import json
from decimal import Decimal


@app.route('/')

@app.route('/index')
def index():
    return render_template('home.html', title='Home')


##########################
@app.route('/new', methods=['GET','POST'])
def new():

    new_dict=uberCopy.get('OptimizedRoute')
    rendered=render_template("Invoice.html",lyft=lyftdata,length=length,uber=uberCopy,min=minuber,minlyft=minlyft,Query=Query,new_dict=new_dict)
    pdf=pdfkit.from_string(rendered,False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='attachment; filename=Invoice.pdf'
    return response
    #eturn render_template("Invoice.html",lyft=lyftdata,length=length,uber=uberCopy,min=minuber,minlyft=minlyft,Query=Query,new_dict=final_dict)


@app.route("/lyft", methods=['GET'])
def Lyft():
    global Query,length,uberdata,minlyft,minuber,lyftdata,uberCopy
    Query = Location.query.all()
    length=len(Query)
    if(length==0):
        return render_template('Results.html',length=length)
    else:
        uberdata = testUber.Uber()
        if(str(uberdata)=='No Data Found'):
            return render_template("")

        else:
            uberCopy = uberdata.copy()
            lyftdata=TestLyft.Lyft()
            length=len(lyftdata)
            print lyftdata
            print uberdata
            print "UberCopy"+str(uberCopy)
            print "###############"
            print "IN Views Functions"
            minuber=GetMin.UberMin(uberdata)
            minlyft=GetMin.Lyftmin(lyftdata)
            print minuber
            print minlyft
            return render_template('Results.html',lyft=lyftdata,length=length,uber=uberdata,min=minuber,minlyft=minlyft,Query=Query)

################################
@app.route("/uber", methods=['GET'])
def Uber():
    test1=testUber.Uber()
    return str(test1)
########################

@app.route('/addplaces',methods=['GET'])
def addplaces():
    x=0
    jsonarray=[]
    dict={}
    dict2={}

    Query=Location.query.all()
    length=len(Query)
    #print length
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
    return render_template('about.html', title='About')    #You can put these attributes on the templates

@app.route('/trip')
def trip():
    global Query,length,uberdata,minlyft,minuber,lyftdata,uberCopy,value,final_dict
    final_dict={}
    Query = Location.query.all()
    length=len(Query)
    if(length==0):
        return render_template('Results.html',length=length)
    else:
        uberdata=testUber.Uber()
        lyftdata=TestLyft.Lyft()
        if(str(uberdata)=="No Data Found" or str(lyftdata)=="No Data Found" ):
            return render_template("ErrorPage.html")

        else:
            length=len(lyftdata)
            uberCopy=uberdata.copy()
            new_dict=uberCopy.get('OptimizedRoute')
            value=""

            for key in new_dict.iteritems():
                id=key[1]['id']
                Send_data=Location.query.filter_by(id=int(id)).first()
                final_dict[int(key[0]+1)]=str(Send_data.address)+","+str(Send_data.city)+","+str(Send_data.state)+","+str(Send_data.zip)
                value=str(value)+str(int(key[0]+1))+": "+str(Send_data.address)+","+str(Send_data.city)+","+str(Send_data.state)+","+str(Send_data.zip)+"\n"

            minuber=GetMin.UberMin(uberdata)
            minlyft=GetMin.Lyftmin(lyftdata)
            user = User.query.filter_by(email=session['email']).first()
            # Send the message
            msg = Message('Trip Planner', sender='loco_perro@rocketmail.com',
                      recipients=[user.email,''])
            message_route = "Optimized Root"+value #PUT HERE THE VALUE
            msg.body = """
                                      From: %s <%s>
                                      %s
                                      """ % ("Trip-Planner app", 'master@trip_planner.com', message_route)
            mail.send(msg)
            print('Message sent')
            return render_template('Results.html',lyft=lyftdata,length=length,uber=uberdata,min=minuber,minlyft=minlyft,Query=Query,way_set=final_dict)


@app.route('/places', methods=['GET', 'POST'])
def places():
    form = PlacesForm()

    # Create a User by default
    Check=len(User.query.all())
    if(Check > 0):
        user = User.query.filter_by(email=session['email']).first()
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

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if form.validate():
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            return redirect(url_for('profile'))
        else:
            flash('All fields are required.')
            return render_template('signup.html', title='Sign Up', form=form)

    elif request.method == 'GET':
        return render_template('signup.html', title='Sign Up', form=form)

@app.route('/profile')
def profile():

    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email=session['email']).first()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if form.validate():
            session['email'] = form.email.data
            return redirect(url_for('profile'))
        else:
            return render_template('signin.html', form=form)
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('index'))


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



@app.route('/trips', methods=['POST'])
def trips_POST():
    if request.method == 'POST':
        print 'INSIDE RESTFUL FUNCTION------------------------------------------------------------'

        global startLat, startLng, jsonarray, finalpath, test, midlength, startid, endId, sequence, endLat, endLng, endId, location
        # Get the data from Request Body
        request_trip = json.loads(request.data)

        start_id = request_trip["start"].split('/')[2]
        end_id = request_trip["end"].split('/')[2]
        others_id = []
        for x in request_trip['others']:
            others_id.append(x.split('/')[2])
        print 'request trip[other]:'+str(request_trip['others'])
        lat=[]
        lng=[]
        # first point
        lat.append(Location.query.filter_by(id=start_id).first().lat)
        lng.append(Location.query.filter_by(id=start_id).first().lng)
        Location.query.filter_by(id=start_id).first().is_end_point = '1'
        # for mid points
        for x in others_id:
            lat.append(Location.query.filter_by(id=x).first().lat)
            lng.append(Location.query.filter_by(id=x).first().lng)
            Location.query.filter_by(id=x).first().is_end_point='0'

        # last point
        lat.append(Location.query.filter_by(id=end_id).first().lat)
        lng.append(Location.query.filter_by(id=end_id).first().lng)
        Location.query.filter_by(id=end_id).first().is_end_point = '2'
        # save all changes to database
        db.session.commit()

        Query = Location.query.all()

        # UBER CALLING CODE---------------------------------------------------------------------------------------
        uberdata = testUber.Uber()
        print uberdata
        print uberdata['uberX']['Miles']

        # LYFT API CODE-----------------------------------------------------------------------------------------


        jsonarray = {}
        dictstart = {}
        dictend = {}
        finalpath = {}
        count = 0
        Query = Location.query.all();


        length = len(Query)

        print length
        for x in range(length):
            if Query[x].is_end_point == 0 and str(Query[x].id) in others_id :  # MId Queryints value
                dictmid = {"lat": Query[x].lat, "lng": Query[x].lng, "id": Query[x].id}
                jsonarray[Query[x].id] = dictmid

            elif Query[x].is_end_point == 1 and str(Query[x].id) == str(start_id):  # Start points value
                startLat = str(Query[x].lat)
                startLng = str(Query[x].lng)
                startid = str(Query[x].id)

            elif Query[x].is_end_point == 2 and str(Query[x].id) == str(end_id):  # End points value
                endLat = str(Query[x].lat)
                endLng = str(Query[x].lng)
                endId = str(Query[x].id)

                # -------------------------------------------------------------------------------------------------------------
        print "jsonarray" + str(jsonarray)

        midL = {}
        midlength = len(jsonarray)
        if (int(midlength) > 0 and int(midlength) != 1):

            while midlength > 1:
                print"Loop" + str(count)
                way = {}
                for key in jsonarray.iteritems():
                    lat = key[1]['lat']
                    lng = key[1]['lng']
                    id = key[1]['id']
                    test = TestLyft.lyftcall(startLat, startLng, lat, lng)

                    way[str(startid) + "-" + str(id)] = int(test)
                    print "way=" + str(way)
                minvalue = min(way, key=way.get)
                test = int(minvalue.split("-")[-1])
                print "test" + str(test)
                if test in jsonarray: del jsonarray[test]
                print jsonarray
                midlength = len(jsonarray)
                print "midlength" + str(midlength)
                Data = Location.query.filter_by(id=test).first()
                startLat = Data.lat
                startLng = Data.lng
                startid = Data.id
                print str(startLat)
                print str(startLng)
                count = count + 1
                finalpath[count] = minvalue

            count = count + 1
            finalpath[count] = str(test) + "-" + str(jsonarray.keys()[0])
            count = count + 1
            finalpath[count] = str(jsonarray.keys()[0]) + "-" + str(endId)
            print "Finalpath" + str(finalpath)
            test = {}
            sequence = 1
            for key in finalpath.iteritems():
                test[sequence] = str(key[1].split("-")[0])
                sequence = sequence + 1
            location = 0;
            id_set = []
            for key in test.iteritems():
                FinalQuery = Location.query.filter_by(id=int(key[1])).first()
                midL[location] = {'lat': FinalQuery.lat, 'lon': FinalQuery.lng}
                id_set.append(FinalQuery.id)
                location += 1

            midL[location] = {'lat': endLat, 'lon': endLng}
        elif (int(midlength) == 1):
            print jsonarray.values()[0]['lat']
            midL[0] = {'lat': startLat, 'lon': startLng}
            midL[1] = {'lat': jsonarray.values()[0]['lat'], 'lon': jsonarray.values()[0]['lng']}
            midL[2] = {'lat': endLat, 'lon': endLng}
            print "json with One Location" + str(jsonarray)
            id_set=[]


        else:
            midL[0] = {'lat': startLat, 'lon': startLng}
            midL[1] = {'lat': endLat, 'lon': endLng}

        print "MIDDLE" + str(midL)


        print "jsonarray" + str(jsonarray)

        # CREATING STRING FOR THE OPTIMIZED ROUTE

        l = len(midL)
        strng = str(l)

        for x in range(l):
            strng += ',' + str(midL[x]['lat']) + ',' + str(midL[x]['lon'])
        print 'string:' + strng

        # -----------------------------------------------------------------
        # lyft api logic
        lat = []
        lng = []
        cords = strng.split(',')

        # fetching the no of locations to be covered
        no_of_cords = int(cords[0])
        count = 0

        # setting the lat and lng list from the string given as a parameter
        while count < no_of_cords:
            lat.append(cords[(2 * count) + 1])
            lng.append(cords[(2 * count) + 2])

            count += 1

        # dictionary for each type of ride
        lyft = {'min_cost': 0,
                'max_cost': 0,
                'avg_cost': 0,
                'time': 0,
                'distance': 0,
                'type': 'lyft'
                }
        lyft_plus = {'min_cost': 0,
                     'max_cost': 0,
                     'avg_cost': 0,
                     'time': 0,
                     'distance': 0,
                     'type': 'lyft_plus'
                     }
        lyft_premier = {'min_cost': 0,
                        'max_cost': 0,
                        'avg_cost': 0,
                        'time': 0,
                        'distance': 0,
                        'type': 'lyft_premier'
                        }
        # making call for ride between each 2 sets of (lat,lng)
        count = 0
        while count != (no_of_cords - 1):
            payload = {'start_lat': lat[count], 'start_lng': lng[count], 'end_lat': lat[count + 1],
                       'end_lng': lng[count + 1]}
            headers = {
                'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
                'Accept-Language': 'en_US', 'Content-Type': 'application/json', }
            stop = requests.get(
                'https://api.lyft.com/v1/cost?',
                headers=headers, params=payload)
            # print stop.json()
            result = stop.json()
            count += 1

            # assigning values in the dictionary
            for iteration in result["cost_estimates"]:
                if iteration["ride_type"] == "lyft_plus":
                    lyft_plus["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft_plus["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft_plus["time"] += iteration["estimated_duration_seconds"]
                    lyft_plus["distance"] += Decimal(iteration["estimated_distance_miles"]).quantize(
                        Decimal("0.01"))
                    # yield lyft_plus
                elif iteration["ride_type"] == "lyft":
                    lyft["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft["time"] += iteration["estimated_duration_seconds"]
                    lyft["distance"] += Decimal(iteration["estimated_distance_miles"]).quantize(Decimal("0.01"))
                    # yield lyft
                elif iteration["ride_type"] == "lyft_premier":
                    lyft_premier["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft_premier["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft_premier["time"] += iteration["estimated_duration_seconds"]
                    lyft_premier["distance"] += Decimal(iteration["estimated_distance_miles"]).quantize(
                        Decimal("0.01"))
                    # yield lyft_premier
        # FINDING THE AVERAGE COST
        a = (lyft['max_cost'] + lyft['min_cost']) / 2
        lyft['avg_cost'] = Decimal(a * 0.01).quantize(Decimal("0.01"))
        b = (lyft_plus['max_cost'] + lyft_plus['min_cost']) / 2
        lyft_plus['avg_cost'] = Decimal(b * 0.01).quantize(Decimal("0.01"))
        c = (lyft_premier['max_cost'] + lyft_premier['min_cost']) / 2
        lyft_premier['avg_cost'] = Decimal(c * 0.01).quantize(Decimal("0.01"))

        lyft_premier["min_cost"] = Decimal(lyft_premier["min_cost"] * 0.01).quantize(Decimal("0.01"))
        lyft["min_cost"] = Decimal(lyft["min_cost"] * 0.01).quantize(Decimal("0.01"))
        lyft_plus["min_cost"] = Decimal(lyft_plus["min_cost"] * 0.01).quantize(Decimal("0.01"))
        lyft_premier["max_cost"] = Decimal(lyft_premier["max_cost"] * 0.01).quantize(Decimal("0.01"))
        lyft["max_cost"] = Decimal(lyft["max_cost"] * 0.01).quantize(Decimal("0.01"))
        lyft_plus["max_cost"] = Decimal(lyft_plus["max_cost"] * 0.01).quantize(Decimal("0.01"))

        print "FULL TRIP STATISTICS"
        print "For lyft:", lyft
        print "For lyft_plus:", lyft_plus
        print "For lyft_premier:", lyft_premier
        # all={'lyft':lyft,'lyft_plus':lyft_plus,'lyft_premier':lyft_premier, 'string':strng,'way':way}
        all = {'lyft': lyft, 'lyft_plus': lyft_plus, 'lyft_premier': lyft_premier}
        print all
        print 'RETURNING FROM THE FUNCTION'

        # --------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------
        b_route = []

        del midL[0]
        m = len(midL)
        del midL[m]

        if len(request_trip['others']) == 0:
            print 'no midpoint'
        elif(len(id_set) == 0):
            r = request_trip['others'][0]
            z = r.split('/')[2]
            b_route.append('/locations/' + str(z))
        else:
            print 'id_set:'+str(id_set)
            print 'midl:'+str(midL)+'len:'+str(len(midL))
            x = 1
            print midL[x]['lat']


            while x<=(len(id_set)-1) :
                a = id_set[x]
                q = Location.query.filter_by(id=a).first()
                print 'q:'+str(q)
                b_route.append('/locations/'+str(q.id))
                x += 1
        # best_route =[]
        # best_route.append(request_trip["start"])
        # way = all["way"]
        # print 'way'+str(way)
        #
        # for x in way:
        #     print 'way in loop:'+str(x)
        #     print 'reqtrip[other]:'+str(request_trip["others"])
        #     best_route.append(request_trip["others"][int(x)])
        # best_route.append(request_trip["end"])

        lyft_db = {
            "name": "Lyft",
            "total_costs_by_cheapest_car_type": float(lyft['avg_cost']),
            "currency_code": "USD",
            "total_duration": int(lyft['time']) / 60,
            "duration_unit": "minute",
            "total_distance": round(lyft['distance'], 2),
            "distance_unit": "mile"

        }
        uber_db = {

            "name": "Uber",
            "total_costs_by_cheapest_car_type": float(uberdata['uberX']['Price']),
            "currency_code": "USD",
            "total_duration": int(float(uberdata['uberX']['Time'])),
            "duration_unit": "minute",
            "total_distance": float(uberdata['uberX']['Miles']),
            "distance_unit": "mile"
        }
        providers=[]
        # INSERTING INTO DB
        t = Trips(str(request_trip['start']),str(b_route),str(request_trip['end']),str(uber_db),str(lyft_db))
        db.session.add(t)
        db.session.commit()


        # GETTING THE RESULT FORMAT READY--------------------------------------------------------------------------
        final_result = {
            "id": t.id,
            "start": request_trip["start"],
            "best_route_by_costs": b_route,
            "providers": [
                {
                    "name": "Uber",
                    "total_costs_by_cheapest_car_type": float(uberdata['uberX']['Price']),
                    "currency_code": "USD",
                    "total_duration": int(float(uberdata['uberX']['Time'])),
                    "duration_unit": "minute",
                    "total_distance": float(uberdata['uberX']['Miles']),
                    "distance_unit": "mile"
                },
                {
                    "name": "Lyft",
                    "total_costs_by_cheapest_car_type": float(lyft['avg_cost']),
                    "currency_code": "USD",
                    "total_duration": int(lyft['time'])/60,
                    "duration_unit": "minute",
                    "total_distance": round(lyft['distance'],2),
                    "distance_unit": "mile"
                }
            ],
            "end": request_trip["end"]

        }
        print 'FINAL RESULT'+str(final_result)
        return make_response(json.dumps(final_result), 200)
