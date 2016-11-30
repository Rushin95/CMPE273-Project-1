from flask import render_template, redirect, request, flash, url_for, json
from flask_mail import Message
from flask_googlemaps import Map, icons

from google_api import *
from forms import *
from myapp import app, mail, db     #import variables created in __init__.py

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

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
        jsonarray.append(dict.copy())
    return render_template('addplaces.html',data=jsonarray)

@app.route('/deleteaddress',methods=['GET', 'POST','Delete'])
def deleteadd():
    uid=request.form.get('x')
    print uid
    Delete_data=Location.query.filter_by(id=uid).first()
    endpt=Delete_data.is_end_point
    if(endpt==1):
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
            print form.Endpoint.data
            obj = GoogleAPI(form.name.data, data[0], data[1], data[2], data[4], int(form.Endpoint.data))
            coordinate = obj.get_coordinates()

            #Add point to the map
            point_info = data[0] + ", " + data[1] + ", " + data[2] + ", " + data[4]
            point = (coordinate.get('lat'), coordinate.get('lng'), point_info)
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
def locations():
    if request.method == 'POST':
        # Get the data from Request Body
        request_data = json.loads(request.data)

        # Get the expense's information from Request Body
        location_name = request_data['name']
        location_address = request_data['address']
        location_city = request_data['city']
        location_state = request_data['state']
        location_zip = request_data['zip']
