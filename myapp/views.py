from flask import render_template, redirect, request, flash, url_for
from flask_mail import Message
from flask_googlemaps import Map, icons

from google_api import *
from forms import *
from myapp import app, mail, db     #import variables created in __init__.py

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

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
    locations = Location.query.all()
    for loc in locations:
        lat = loc.lat
        lng = loc.lng
        point_info = loc.address + ", " + loc.city + ", " + loc.state + ", " + unicode(loc.zip)
        point = (lat, lng, point_info)
        if(loc.is_end_point):
            my_markers[icons.dots.red].append(point)
        else:
            my_markers[icons.dots.green].append(point)

    if request.method == 'POST':        ##capture the form field data and check if it's valid
        if form.validate():
            #print form.Gaddress.data
            data = [x.strip() for x in form.Gaddress.data.split(',')]
            #If invalid Address Format
            if len(data) != 5:
                flash('Invalid Address format. Allowed Format: Street Address, City, State, Country, Zipcode')
                mymap = Map(identifier="mymap", varname="mymap", lat=app.config['LAT'], lng=app.config['LNG'],
                            style="width:400px;height:400px;margin:50;", markers=my_markers, zoom=9)
                return render_template('places.html', title='Places', form=form, mymap=mymap)

            #Get latitude and longitude and Store point into the DB
            obj = GoogleAPI(form.name.data, data[0], data[1], data[2], data[4], False)
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
            return render_template('places.html', title='Places', form=form, mymap=mymap)

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
        # Create Map after have the markers defined. Cuase it put markers only when create map object
        # identifier for DOM element, varname for JS object name
        mymap = Map(identifier="mymap", varname="mymap", lat=app.config['LAT'], lng=app.config['LNG'],
                    style="width:400px;height:400px;margin:50;", markers=my_markers, zoom=9)
        # initial GET use render_template
        return render_template('places.html', title='Places', form=form, mymap=mymap)

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
