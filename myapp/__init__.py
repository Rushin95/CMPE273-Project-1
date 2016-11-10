# __init__.py makes Python treat our directory as a package and allows us to include some code.
from flask import Flask

# Load configuration variables from an instance folder (allows us to store sensible data like keys)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#Regular Configuration
#app = Flask(__name__)
#app.config.from_object('config')        # Now we can access the configuration variables via app.config["VAR_NAME"].

from myapp import views


