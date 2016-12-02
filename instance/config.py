import os
#We can access variables from config.py using --> app.config["VAR_NAME"].

#Configure MySQL
DB_USER = 'root'
<<<<<<< HEAD
DB_PASSWORD = 'supersecure'
=======
DB_PASSWORD = '1q2w3e4r'
>>>>>>> a99c3c7965186e3cbe19a97696d63891dd1ca3bd
DB_NAME = 'development'
#DB_HOSTNAME = 'mysqlserver'		#docker-compose.yml hostname
DB_HOSTNAME = 'localhost'           #for local use
DB_URI = 'mysql://%s:%s@%s/%s'%(DB_USER, DB_PASSWORD, DB_HOSTNAME, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Configure WTF
# The WTF_CSRF_ENABLED setting activates the cross-site request forgery prevention
# The SECRET_KEY is used to create a cryptographic token that is used to validate a form.
WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

#Config Mail
MAIL_FROM_EMAIL = "juancpinzone@hotmail.com" # For use in application emails
MAIL_SERVER = "smtp.mail.yahoo.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'loco_perro@rocketmail.com'
MAIL_PASSWORD = 'SuperSecure2016Password'


#Configure Googlge Key required to connect GoogleMaps API
GOOGLEMAPS_KEY = 'AIzaSyBYsJ3ig9aPJCgfk45XqRj-ZfqreytYC-w'
