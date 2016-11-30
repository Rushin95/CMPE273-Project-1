from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField, StringField, PasswordField,SelectField
from flask_wtf import Form
from wtforms.validators import *     #so you call validators directly, instead of using validators.blahblah

from models import User


class PlacesForm(FlaskForm):
    name = StringField("Name", [InputRequired("Please enter your name.")])
    Gaddress = StringField("Address", [InputRequired("Please enter your Address.")])
    Endpoint = SelectField('Type', choices = [('0', 'Other'), ('1', 'Start'), ('2', 'End')], default='0')
    submit = SubmitField("Add Place")


class SignupForm(FlaskForm):
    firstname = StringField("First name", [InputRequired("Please enter your first name.")])
    lastname = StringField("Last name", [InputRequired("Please enter your last name.")])
    email = StringField("Email", [InputRequired("Please enter your email address."), Email("Please enter a valid email address."), EqualTo('confirm_email', message='Emails must match')])
    confirm_email = StringField("Confirm Email", [InputRequired("Please confirm your email address."), Email("Please confirm with a valid email address.")])
    password = PasswordField('Password', [InputRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    #Constructor that just calls the base class' constructor (FlaskForm is the base class)
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    #ensures an account does not already exist with the user's email address (username)
    def validate(self):
        if not FlaskForm.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True
