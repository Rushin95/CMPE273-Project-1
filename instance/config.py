#Configure MySQL
SQLALCHEMY_DATABASE_URI= \
"mysql://root:supersecure@localhost/cmpe273"

#Configure WTF
# The WTF_CSRF_ENABLED setting activates the cross-site request forgery prevention
# The SECRET_KEY is used to create a cryptographic token that is used to validate a form.
WTF_CSRF_ENABLED = True
SECRET_KEY = 'Cm9obiBTY2hyb20fa3rjo3MgABNz'

GOOGLE_KEY = 'AIzaSyDTjklW141YfMMJh7BWWllamhPRsOD6LuU'

#STRIPE_API_KEY = 'SmFjb2IgS2FwbGFuLU1vc3MgaXMgYSBoZXJv'