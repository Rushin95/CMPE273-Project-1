from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField, StringField
from wtforms.validators import *

class ContactForm(FlaskForm):
    name = StringField("Name", [InputRequired()])
    email = StringField("Email", [InputRequired(), Email(),EqualTo('confirm_email', message='Emails must match')])
    confirm_email = StringField("Email", [InputRequired(), Email()])
    subject = StringField("Subject", [InputRequired()])
    message = TextAreaField("Message", [InputRequired()])
    submit = SubmitField("Send")

class LoginForm(FlaskForm):
    openid = StringField("Please enter your OpenID", [InputRequired()])         #DataRequired validator simply checks that the field is not submitted empty
    remember_me = BooleanField("Remember Me", default=False)
    sign_in = SubmitField("Sign In")

class LocationsForm(FlaskForm):
    name = StringField("Name", [InputRequired()])
    address = StringField("Adress", [InputRequired()])
    city = StringField("City", [InputRequired()])
    state = StringField("State", [InputRequired()])
    zip = StringField("ZipCode", [InputRequired()])
    submit = SubmitField("Send")