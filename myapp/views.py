from flask import render_template, redirect, request, flash
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
    # creating a map in the view

    #Import markers from DB
    my_markers = {
        icons.dots.green: [(37.4419, -122.1419, "AddressGreen1"), (37.4500, -122.1350, "AddressGreen2")],
        icons.dots.red: [(37.4300, -122.1400, "AddressRed")]
    }
    mymap = Map(
        identifier="mymap",  # for DOM element
        varname="mymap",  # for JS object name
        lat=37.4419,
        lng=-122.1419,
        style="width:400px;height:400px;margin:50;",
        markers=my_markers
    )

    if request.method == 'POST':        ##capture the form field data and check if it's valid
        if form.validate():
            obj = GoogleAPI(form.name.data, form.address.data, form.city.data, form.state.data, form.zip.data)
            print(obj.google())
            return render_template('places.html', title='Places', form=form, mymap=mymap)
        else:
            flash('All fields are required.')
            return render_template('places.html', title='Places', form=form, mymap=mymap)

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
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
