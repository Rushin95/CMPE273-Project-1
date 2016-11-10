from myapp import app
from google_api import *
from flask import render_template, request, flash
from forms import ContactForm, LoginForm, LocationsForm

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':        ##capture the form field data and check if it's valid
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', title='Contact', form=form)
        else:
            return 'Form posted.'

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
        return render_template('contact.html', title='Contact', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':        ##capture the form field data and check if it's valid
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('login.html', title='Login', form=form)
        else:
            return 'Form posted.'

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
        return render_template('login.html', title='Login', form=form)


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    form = LocationsForm()

    if request.method == 'POST':        ##capture the form field data and check if it's valid
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('locations.html', title='Locations', form=form)
        else:
            obj = GoogleAPI(form.name.data, form.address.data, form.city.data, form.state.data, form.zip.data)
            print(obj.google())
            return 'obj.google()'

    elif request.method == 'GET':       # else, form should be retrieved and loaded in browser
        return render_template('locations.html', title='Locations', form=form)