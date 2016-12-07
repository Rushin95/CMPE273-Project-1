import bcrypt
from myapp import db            #means --> From model.py import variable db

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    location = db.relationship("Location")

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    def validate_password(self, password):
        return bcrypt.hashpw((password.encode('utf-8')).encode('utf-8'), self.password.encode('utf-8')) == self.password.encode('utf-8')
#        return bcrypt.hashpw(password.encode('utf-8'), self.password.encode('utf-8').decode()) == self.password

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    #country=db.column(db.String(50))
    zip =  db.Column(db.String(20))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    is_end_point = db.Column(db.Integer, unique=False, default=0)

    def __init__(self, user_id, name, address, city, state,zip, lat, lng, is_end_point):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        #self.country=country
        self.zip = zip
        self.lat = lat
        self.lng = lng
        self.is_end_point = is_end_point


class Trips(db.Model):
    __tablename__ = 'trip'
    id = db.Column(db.Integer, primary_key = True)
    start = db.Column(db.String(300))
    best_route = db.Column(db.String(1000))
    end = db.Column(db.String(300))
    uber = db.Column(db.String(5000))
    lyft = db.Column(db.String(5000))

    def __init__(self, start, best_route, end, uber, lyft):
        self.start = start
        self.best_route = best_route
        self.end = end
        self.uber = uber
        self.lyft = lyft
