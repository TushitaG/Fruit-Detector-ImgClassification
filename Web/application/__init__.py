from flask import Flask
from flask_cors import CORS
#For persistent storage
from flask_sqlalchemy import SQLAlchemy
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
 
#create the Flask app
app = Flask(__name__)
 
# load configuration from config.cfg
if "TESTING" in os.environ:
    app.config.from_envvar('TESTING')
    print("Using config for TESTING")
elif "DEVELOPMENT" in os.environ:
    app.config.from_envvar('DEVELOPMENT')
    print("Using config for DEVELOPMENT")
else:
    app.config.from_pyfile('config_dply.cfg')
    print("Using config for deployment")
CORS(app)
# instantiate SQLAlchemy to handle db process
db = SQLAlchemy(app)
 
# Upload images to database
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

#run the file routes.py
from application import routes

