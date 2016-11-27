# __init__.py makes Python treat our directory as a package and allows us to include some code.
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_googlemaps import GoogleMaps


# Load configuration variables from an instance folder (allows us to store sensible data like keys)
app = Flask(__name__, instance_relative_config=True)
mail = Mail()
db = SQLAlchemy()
google_maps = GoogleMaps()
app.config.from_object('config')
app.config.from_pyfile('config.py')

#Regular Configuration
#app = Flask(__name__)
#app.config.from_object('config')        # Now we can access the configuration variables via app.config["VAR_NAME"].

mail.init_app(app)
db.init_app(app)
google_maps.init_app(app)


@app.before_first_request
def initialize_database():
    # Create DataBase and Tablets if not exist
    engine = create_engine(app.config['DB_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    engine.execute("DROP DATABASE %s "%(app.config['DB_NAME']))
    engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(app.config['DB_NAME']))
    db.create_all()                     #create the tables
    db.session.commit()

from myapp import views, models         #MUST be last line on file


