from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
import pdfkit
from myapp import TestLyft
from myapp import testUber
from myapp import GetMin
from myapp import app, mail, db  #import variables created in __init__.py
import json
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


@app.route("/lyft", methods=['GET'])
def Lyft():
    global Query,length,uberdata,minlyft,minuber,lyftdata,uberCopy
    Query = Location.query.all()
    length=len(Query)
    if(length==0):
        return render_template('Results.html',length=length)
    else:
        lyftdata=TestLyft.Lyft(Query)
        length=len(lyftdata)
        uberdata=testUber.Uber()
        uberCopy=uberdata.copy()
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



@app.route('/trips', methods=['POST'])
def trips_POST():
    if request.method == 'POST':


        # Get the data from Request Body
        request_trip = json.loads(request.data)

        start_id = request_trip["start"].split('/')[2]
        end_id = request_trip["end"].split('/')[2]
        others_id = []

        for x in request_trip['others']:
            others_id.append(x.split('/')[2])

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
        lyft_result = TestLyft.Lyft(Query)
        way = lyft_result["way"]



        best_route =[]
        best_route.append(request_trip["start"])
        for x in way:
            best_route.append(request_trip["others"][int(x)])
        best_route.append(request_trip["end"])
        # GETTING THE RESULT FORMAT READY
        final_result = {
            "id": 200000,
            "start": request_trip["start"],
            "best_route_by_costs": best_route,
            "providers": [
                {
                    "name": "Uber",
                    "total_costs_by_cheapest_car_type": 125,
                    "currency_code": "USD",
                    "total_duration": 640,
                    "duration_unit": "minute",
                    "total_distance": 25.05,
                    "distance_unit": "mile"
                },
                {
                    "name": "Lyft",
                    "total_costs_by_cheapest_car_type": float(lyft_result['lyft']['avg_cost']),
                    "currency_code": "USD",
                    "total_duration": int(lyft_result['lyft']['time'])/60,
                    "duration_unit": "minute",
                    "total_distance": float(lyft_result['lyft']['distance']),
                    "distance_unit": "mile"
                }
            ],
            "end": request_trip["end"]

        }
        print final_result
        return make_response(json.dumps(final_result), 200)
